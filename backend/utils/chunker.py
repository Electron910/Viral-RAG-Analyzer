from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict, Any

def chunk_transcript(transcript: str, metadata: Dict[str, Any], video_id: str, session_id: str) -> List[Dict[str, Any]]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len
    )
    
    chunks = splitter.split_text(transcript)
    
    documents = []
    for i, chunk in enumerate(chunks):
        chunk_metadata = metadata.copy()
        chunk_metadata["video_id"] = video_id
        chunk_metadata["session_id"] = session_id
        chunk_metadata["chunk_index"] = i
        
        clean_metadata = {}
        for k, v in chunk_metadata.items():
            if isinstance(v, list):
                if not v:
                    continue
                clean_metadata[k] = ", ".join([str(item) for item in v])
            elif v is None:
                continue
            else:
                clean_metadata[k] = v
                
        documents.append({
            "page_content": chunk,
            "metadata": clean_metadata
        })
        
    return documents
