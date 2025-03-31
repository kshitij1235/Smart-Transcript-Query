from fastapi import APIRouter
from app.api.dependency import *
from app.api.service import *
from app.database import redis_client

router = APIRouter(prefix="/api")

@router.get("/extract_transcript")
async def extract_transcript(
    video_url: str
):
    """
    Extract transcript from a YouTube URL and cache it.
    """
    data = BatchProcessing(video_url).process_query()
    if data is None :
        return {"status":"info","data":"The video has no transcribe"}
    
    return {"status":"success","data":data}

@router.delete("/clear_cache")
async def clear_cache(transcript_id: str):
    """
    Clears the cached transcript for the given transcript_id.
    """
    data =redis_client.get("transcribe")
    redis_client.flushdb()
    return {
        "status":"success",
        "message":"cache cleared",
        "data":data
    }

@router.post("/ask_questions")
async def ask_questions():
    """
    Accepts a transcript_id and a batch of questions, then returns answers processed asynchronously.
    """
    ...

@router.get("/status")
async def status():
    return {"status": "API is running"}
