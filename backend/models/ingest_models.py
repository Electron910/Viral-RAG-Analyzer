from pydantic import BaseModel
from typing import Optional
from typing import List, Dict, Any

class VideoInput(BaseModel):
    platform: str
    url: str

class IngestRequest(BaseModel):
    videos: List[VideoInput]

class IngestResponse(BaseModel):
    session_id: str
    metadata_list: List[Dict[str, Any]]
