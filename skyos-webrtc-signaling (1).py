import json
import logging
import asyncio
from typing import Dict, Set, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, APIRouter
from pydantic import BaseModel

# ------------------------------------------------------------------------------
# SkyOS WebRTC Avatar Streaming - FastAPI Signaling Gateway
# ------------------------------------------------------------------------------
# Handhabt den SDP (Offer/Answer) & ICE Candidate Austausch zwischen der
# Flutter Mobile Steuerzentrale und dem Python Avatar Render Engine Backend.
# ------------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SkyOSWebRTCSignaling")

router = APIRouter(prefix="/ws/v1/avatar", tags=["Avatar WebRTC Signaling"])


class SignalingMessage(BaseModel):
    """Datenmodell für WebRTC Signaling Nachrichten über WebSocket."""
    type: str  # 'offer', 'answer', 'candidate', 'control', 'ping', 'pong'
    session_id: str
    sender: str  # 'flutter_client' oder 'avatar_engine'
    sdp: Optional[str] = None
    candidate: Optional[Dict] = None
    control_action: Optional[str] = None  # 'start_stream', 'stop_stream', 'pause_video'
    metadata: Optional[Dict] = None


class AvatarSignalingManager:
    """Verwaltet aktive WebRTC-Signaling-Sessions zwischen Flutter App & Avatar Renderer."""

    def __init__(self):
        # Maps session_id -> Dict of WebSocket connections {'flutter_client': ws, 'avatar_engine': ws}
        self.active_sessions: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(self, session_id: str, client_type: str, websocket: WebSocket):
        await websocket.accept()
        if session_id not in self.active_sessions:
            self.active_sessions[session_id] = {}
        
        self.active_sessions[session_id][client_type] = websocket
        logger.info(f"WebRTC Signaling Verbindung aufgebaut: Session '{session_id}' | Client: '{client_type}'")

        # Benachrichtige Gegenstelle, dass die Verbindung bereit ist
        peer_type = 'avatar_engine' if client_type == 'flutter_client' else 'flutter_client'
        if peer_type in self.active_sessions[session_id]:
            await self.send_to_peer(
                session_id,
                peer_type,
                {
                    "type": "control",
                    "session_id": session_id,
                    "sender": "system",
                    "control_action": "peer_connected",
                    "metadata": {"peer": client_type}
                }
            )

    def disconnect(self, session_id: str, client_type: str):
        if session_id in self.active_sessions:
            if client_type in self.active_sessions[session_id]:
                del self.active_sessions[session_id][client_type]
                logger.info(f"Client '{client_type}' aus Session '{session_id}' getrennt.")
            
            if not self.active_sessions[session_id]:
                del self.active_sessions[session_id]
                logger.info(f"Session '{session_id}' vollständig geschlossen.")

    async def send_to_peer(self, session_id: str, target_client: str, message: dict):
        """Sendet ein Signaling-Paket gezielt an den jeweiligen Peer (Client <-> Engine)."""
        if session_id in self.active_sessions and target_client in self.active_sessions[session_id]:
            target_ws = self.active_sessions[session_id][target_client]
            await target_ws.send_text(json.dumps(message))
        else:
            logger.warning(f"Peer '{target_client}' in Session '{session_id}' nicht erreichbar!")


signaling_manager = AvatarSignalingManager()


@router.websocket("/webrtc/{session_id}/{client_type}")
async def avatar_webrtc_signaling_endpoint(
    websocket: WebSocket,
    session_id: str,
    client_type: str  # Muss 'flutter_client' oder 'avatar_engine' sein
):
    """
    WebSocket-Endpunkt für das WebRTC-Signaling.
    Ablauf:
    1. Flutter sendet WebRTC Offer (SDP)
    2. Avatar Engine antwortet mit WebRTC Answer (SDP)
    3. Beide tauschen kontinuierlich ICE Candidates für NAT-Traversal aus.
    """
    if client_type not in ["flutter_client", "avatar_engine"]:
        await websocket.close(code=4000, reason="Ungültiger client_type. Erlaubt: 'flutter_client' oder 'avatar_engine'")
        return

    await signaling_manager.connect(session_id, client_type, websocket)
    target_peer = "avatar_engine" if client_type == "flutter_client" else "flutter_client"

    try:
        while True:
            raw_data = await websocket.receive_text()
            try:
                data_dict = json.loads(raw_data)
                msg = SignalingMessage(**data_dict)

                logger.debug(f"[{session_id}] Signaling Typ '{msg.type}' von '{client_type}' -> '{target_peer}'")

                # Handle Ping/Heartbeat
                if msg.type == "ping":
                    await websocket.send_text(json.dumps({"type": "pong", "session_id": session_id}))
                    continue

                # Weiterleitung des WebRTC SDP Offers / Answers / ICE Candidates an den Peer
                await signaling_manager.send_to_peer(
                    session_id=session_id,
                    target_client=target_peer,
                    message=msg.model_dump(exclude_none=True)
                )

            except json.JSONDecodeError:
                logger.error("Ungültiges JSON-Format empfangen.")
                await websocket.send_text(json.dumps({"type": "error", "message": "Invalid JSON format"}))
            except Exception as e:
                logger.error(f"Fehler bei Signaling-Verarbeitung: {e}")
                await websocket.send_text(json.dumps({"type": "error", "message": str(e)}))

    except WebSocketDisconnect:
        signaling_manager.disconnect(session_id, client_type)
        # Informiere Gegenstelle über Verbindungsabbruch
        await signaling_manager.send_to_peer(
            session_id,
            target_peer,
            {
                "type": "control",
                "session_id": session_id,
                "sender": "system",
                "control_action": "peer_disconnected",
                "metadata": {"disconnected_peer": client_type}
            }
        )


# Beispielhafte Einbindung in die Haupt-FastAPI-App
app = FastAPI(title="SkyOS Avatar WebRTC Gateway", version="1.0.0")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
