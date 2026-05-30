import uuid
from typing import Dict, Any

_sessions: Dict[str, Dict[str, Any]] = {}

def create_session() -> str:
    session_id = str(uuid.uuid4())
    _sessions[session_id] = {}
    return session_id

def get_session(session_id: str) -> Dict[str, Any]:
    if session_id not in _sessions:
        _sessions[session_id] = {}
    return _sessions[session_id]
