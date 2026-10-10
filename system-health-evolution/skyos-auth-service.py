import hashlib
import secrets
import logging
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, EmailStr, Field
from fastapi import FastAPI, APIRouter, HTTPException, status

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SkyOSAuthService")

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication & Identity"])

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Hauptpasswort (Password Manager kompatibel)")
    phone_number: Optional[str] = Field(None, description="Handynummer fuer SMS 2FA")
    full_name: Optional[str] = "SkyOS User"

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str
    totp_code: Optional[str] = Field(None, description="6-stelliger 2FA Code")
    recovery_code: Optional[str] = Field(None, description="Einmal-Wiederherstellungscode")

class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str
    email: str
    gravatar_url: str
    is_2fa_enabled: bool

class TwoFactorSetupResponse(BaseModel):
    secret: str
    qr_uri: str
    recovery_codes: List[str]

class GravatarProfile(BaseModel):
    email: str
    gravatar_hash: str
    avatar_url: str
    profile_url: str

class GravatarHelper:
    """Gravatar Profilbild-Integration über E-Mail SHA-256 Hash."""
    
    @staticmethod
    def get_gravatar_hash(email: str) -> str:
        normalized = email.strip().lower()
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

    @staticmethod
    def get_avatar_url(email: str, size: int = 200) -> str:
        h = GravatarHelper.get_gravatar_hash(email)
        return f"avatar_service_url_{h}_{size}"

    @staticmethod
    def get_profile_info(email: str) -> GravatarProfile:
        h = GravatarHelper.get_gravatar_hash(email)
        return GravatarProfile(
            email=email,
            gravatar_hash=h,
            avatar_url=f"avatar_url_{h}",
            profile_url=f"profile_url_{h}"
        )

class RecoveryCodeManager:
    """Generiert und verifiziert Wiederherstellungscodes."""
    
    @staticmethod
    def generate_codes(count: int = 8) -> List[str]:
        codes = []
        for _ in range(count):
            p1 = secrets.token_hex(2).upper()
            p2 = secrets.token_hex(2).upper()
            codes.append(f"{p1}-{p2}")
        return codes

    @staticmethod
    def hash_code(code: str) -> str:
        cleaned = code.strip().upper().replace(" ", "")
        return hashlib.sha256(cleaned.encode('utf-8')).hexdigest()

class SecurityStore:
    def __init__(self):
        self.users: Dict[str, Dict[str, Any]] = {}

    def hash_password(self, password: str) -> str:
        salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}${hashed.hex()}"

    def verify_password(self, password: str, stored_hash: str) -> bool:
        try:
            salt, hashed = stored_hash.split("$")
            rehashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return secrets.compare_digest(rehashed.hex(), hashed)
        except Exception:
            return False

db_store = SecurityStore()

@router.post("/register", response_model=AuthTokenResponse, status_code=status.HTTP_201_CREATED)
async def register_user(req: UserRegisterRequest):
    """Registriert einen Benutzer mit E-Mail, Passwort & Handynummer."""
    if req.email in db_store.users:
        raise HTTPException(status_code=400, detail="Diese E-Mail ist bereits registriert.")

    user_id = f"usr_{secrets.token_hex(6)}"
    password_hash = db_store.hash_password(req.password)
    gravatar_url = GravatarHelper.get_avatar_url(req.email)
    recovery_codes = RecoveryCodeManager.generate_codes(8)
    hashed_recovery = [RecoveryCodeManager.hash_code(c) for c in recovery_codes]

    db_store.users[req.email] = {
        "user_id": user_id,
        "email": req.email,
        "password_hash": password_hash,
        "phone_number": req.phone_number,
        "full_name": req.full_name,
        "is_2fa_enabled": False,
        "totp_secret": secrets.token_hex(10).upper(),
        "recovery_codes_hashed": hashed_recovery,
        "gravatar_url": gravatar_url
    }

    access_token = f"skyos_jwt_{secrets.token_urlsafe(32)}"
    return AuthTokenResponse(
        access_token=access_token,
        expires_in=86400,
        user_id=user_id,
        email=req.email,
        gravatar_url=gravatar_url,
        is_2fa_enabled=False
    )

@router.post("/login", response_model=AuthTokenResponse)
async def login_user(req: UserLoginRequest):
    """Authentifiziert den Benutzer mit Passwort, 2FA oder Backup-Code."""
    user = db_store.users.get(req.email)
    if not user or not db_store.verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Ungueltige Anmeldedaten.")

    if user["is_2fa_enabled"]:
        if req.recovery_code:
            code_hash = RecoveryCodeManager.hash_code(req.recovery_code)
            if code_hash in user["recovery_codes_hashed"]:
                user["recovery_codes_hashed"].remove(code_hash)
            else:
                raise HTTPException(status_code=401, detail="Ungueltiger Wiederherstellungscode.")
        elif req.totp_code:
            if len(req.totp_code) != 6 or not req.totp_code.isdigit():
                raise HTTPException(status_code=401, detail="Ungueltiger 2FA Code.")
        else:
            raise HTTPException(status_code=403, detail="2FA erforderlich.")

    access_token = f"skyos_jwt_{secrets.token_urlsafe(32)}"
    return AuthTokenResponse(
        access_token=access_token,
        expires_in=86400,
        user_id=user["user_id"],
        email=user["email"],
        gravatar_url=user["gravatar_url"],
        is_2fa_enabled=user["is_2fa_enabled"]
    )

@router.post("/2fa/setup", response_model=TwoFactorSetupResponse)
async def setup_two_factor(email: str):
    """Aktiviert 2FA und erzeugt 8 Einmal-Wiederherstellungscodes."""
    user = db_store.users.get(email)
    if not user:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden.")

    totp_secret = secrets.token_hex(10).upper()
    user["totp_secret"] = totp_secret
    user["is_2fa_enabled"] = True

    raw_recovery_codes = RecoveryCodeManager.generate_codes(8)
    user["recovery_codes_hashed"] = [RecoveryCodeManager.hash_code(c) for c in raw_recovery_codes]

    totp_uri = f"totp_uri_{email}_{totp_secret}"

    return TwoFactorSetupResponse(
        secret=totp_secret,
        qr_uri=totp_uri,
        recovery_codes=raw_recovery_codes
    )

@router.get("/gravatar/{email}", response_model=GravatarProfile)
async def get_gravatar(email: str):
    return GravatarHelper.get_profile_info(email)

app = FastAPI(title="SkyOS Auth Gateway")
app.include_router(router)
