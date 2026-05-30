from fastapi import APIRouter
from models.ingest_models import IngestRequest, IngestResponse
from services.youtube_service import fetch_youtube_data
from services.instagram_service import fetch_instagram_data
from services.vectorstore import upsert_chunks
from utils.chunker import chunk_transcript
from utils.session import create_session

router = APIRouter()

@router.post("/ingest", response_model=IngestResponse)
async def ingest_videos(request: IngestRequest):
    session_id = create_session()
    
    all_chunks = []
    metadata_list = []
    
    for idx, video in enumerate(request.videos):
        # Determine video ID label (A, B, C, etc.)
        video_id = chr(65 + idx)
        
        if video.platform == "youtube":
            transcript, metadata = fetch_youtube_data(video.url)
        elif video.platform == "instagram":
            transcript, metadata = fetch_instagram_data(video.url)
        else:
            continue
            
        chunks = chunk_transcript(transcript, metadata, video_id, session_id)
        all_chunks.extend(chunks)
        metadata_list.append(metadata)
        
    if all_chunks:
        upsert_chunks(all_chunks)
    
    return IngestResponse(
        session_id=session_id,
        metadata_list=metadata_list
    )
