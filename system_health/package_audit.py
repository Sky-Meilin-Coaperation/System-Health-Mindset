import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote, urlparse

_REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
_IGNORED_DIRECTORIES = {
    ".git",
    ".dart_tool",
    ".venv",
    "build",
    "dist",
    "venv",
}


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _fingerprint_files(files: Iterable[tuple[str, Path]]) -> tuple[str, int]:
    digest = hashlib.sha256()
    file_count = 0
    for relative_path, file_path in sorted(files, key=lambda item: item[0]):
        try:
            content_digest = _sha256(file_path.read_bytes())
        except OSError as exc:
            raise ValueError(f"Cannot fingerprint installed package file: {relative_path}") from exc
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(content_digest.encode("ascii"))
        digest.update(b"\n")
        file_count += 1
    return digest.hexdigest(), file_count


def _python_packages() -> list[dict[str, Any]]:
    packages = []
    for distribution in importlib.metadata.distributions():
        name = distribution.metadata.get("Name")
        if not name:
            continue
        record = distribution.read_text("RECORD")
        metadata = distribution.read_text("METADATA")
        record_text = record or ""
        metadata_text = metadata or ""
        packages.append(
            {
                "ecosystem": "pip",
                "name": name,
                "version": distribution.version,
                "location": "python-environment",
                "manifest_sha256": _sha256(metadata_text.encode("utf-8")),
                "fingerprint_sha256": _sha256(
                    (record_text or metadata_text).encode("utf-8")
                ),
                "fingerprint_scope": "pip-install-record" if record else "distribution-metadata",
                "file_count": len(record_text.splitlines()) if record else 1,
            }
        )
    return packages


def _npm_roots(repository_root: Path) -> list[Path]:
    roots: list[Path] = []
    for current, directories, _ in os.walk(repository_root):
        directories[:] = [
            name
            for name in directories
            if name not in _IGNORED_DIRECTORIES and name != "node_modules"
        ]
        package_root = Path(current) / "node_modules"
        if package_root.is_dir():
            roots.append(package_root)
    return roots


def _npm_packages(roots: list[Path], repository_root: Path) -> list[dict[str, Any]]:
    packages = []
    for root in roots:
        for current, directories, files in os.walk(root):
            directories[:] = [name for name in directories if name != ".bin"]
            if "package.json" not in files:
                continue
            manifest_path = Path(current) / "package.json"
            try:
                manifest_bytes = manifest_path.read_bytes()
                manifest = json.loads(manifest_bytes)
            except (OSError, json.JSONDecodeError) as exc:
                raise ValueError(f"Cannot audit npm package manifest: {manifest_path}") from exc
            name = manifest.get("name")
            version = manifest.get("version")
            if not isinstance(name, str) or not isinstance(version, str):
                continue
            installed_files = []
            for package_current, package_directories, package_files in os.walk(manifest_path.parent):
                package_directories[:] = [
                    directory
                    for directory in package_directories
                    if directory not in {".git", ".dart_tool"}
                ]
                installed_files.extend(
                    (
                        (Path(package_current) / filename)
                        .relative_to(manifest_path.parent)
                        .as_posix(),
                        Path(package_current) / filename,
                    )
                    for filename in package_files
                )
            content_sha256, file_count = _fingerprint_files(installed_files)
            packages.append(
                {
                    "ecosystem": "npm",
                    "name": name,
                    "version": version,
                    "location": manifest_path.parent.relative_to(repository_root).as_posix(),
                    "manifest_sha256": _sha256(manifest_bytes),
                    "fingerprint_sha256": content_sha256,
                    "fingerprint_scope": "installed-files",
                    "file_count": file_count,
                }
            )
    return packages


def _pub_package_config_paths(repository_root: Path) -> list[Path]:
    configs = []
    for current, directories, files in os.walk(repository_root):
        directories[:] = [
            name
            for name in directories
            if name not in (_IGNORED_DIRECTORIES - {".dart_tool"})
            and name != "node_modules"
        ]
        if "package_config.json" in files and Path(current).name == ".dart_tool":
            configs.append(Path(current) / "package_config.json")
    return configs


def _pub_packages(config_paths: list[Path], repository_root: Path) -> list[dict[str, Any]]:
    packages = []
    for config_path in config_paths:
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"Cannot audit Dart package config: {config_path}") from exc

        for package in config.get("packages", []):
            name = package.get("name")
            root_uri = package.get("rootUri")
            if not isinstance(name, str) or not isinstance(root_uri, str):
                raise ValueError(f"Invalid package entry in Dart config: {config_path}")

            parsed_uri = urlparse(root_uri)
            if parsed_uri.scheme == "file":
                package_root = Path(unquote(parsed_uri.path))
                if os.name == "nt" and package_root.as_posix().startswith("/"):
                    package_root = Path(package_root.as_posix().lstrip("/"))
            elif parsed_uri.scheme:
                raise ValueError(f"Unsupported Dart package URI in {config_path}: {root_uri}")
            else:
                package_root = (config_path.parent / root_uri).resolve()

            pubspec = package_root / "pubspec.yaml"
            try:
                pubspec_content = pubspec.read_bytes()
            except OSError as exc:
                raise ValueError(f"Cannot read installed Dart package manifest: {pubspec}") from exc
            installed_files = []
            for package_current, package_directories, package_files in os.walk(package_root):
                package_directories[:] = [
                    directory
                    for directory in package_directories
                    if directory not in {".git", ".dart_tool"}
                ]
                installed_files.extend(
                    (
                        (Path(package_current) / filename).relative_to(package_root).as_posix(),
                        Path(package_current) / filename,
                    )
                    for filename in package_files
                )
            content_sha256, file_count = _fingerprint_files(installed_files)

            packages.append(
                {
                    "ecosystem": "pub",
                    "name": name,
                    "version": str(package.get("version", "unknown")),
                    "location": config_path.parent.parent.relative_to(repository_root).as_posix()
                    or ".",
                    "manifest_sha256": _sha256(pubspec_content),
                    "fingerprint_sha256": content_sha256,
                    "fingerprint_scope": "installed-files",
                    "file_count": file_count,
                }
            )
    return packages


def collect_installed_packages(
    repository_root: Path | None = None,
) -> dict[str, Any]:
    root = (repository_root or _REPOSITORY_ROOT).resolve()
    python_packages = _python_packages()
    npm_roots = _npm_roots(root)
    npm_packages = _npm_packages(npm_roots, root)
    pub_configs = _pub_package_config_paths(root)
    pub_packages = _pub_packages(pub_configs, root)
    packages = sorted(
        python_packages + npm_packages + pub_packages,
        key=lambda item: (item["ecosystem"], item["location"], item["name"].lower()),
    )
    return {
        "packages": packages,
        "package_count": len(packages),
        "sources": {
            "pip": {"status": "audited", "package_count": len(python_packages)},
            "npm": {
                "status": "audited" if npm_roots else "no_node_modules_found",
                "install_roots": len(npm_roots),
                "package_count": len(npm_packages),
            },
            "pub": {
                "status": "audited" if pub_configs else "no_package_config_found",
                "package_configs": len(pub_configs),
                "package_count": len(pub_packages),
            },
        },
    }
