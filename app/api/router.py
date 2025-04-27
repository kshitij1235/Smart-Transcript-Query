from fastapi import APIRouter
from app.api.dependency import *
from app.api.service import *
# from app.database import redis_client
from app.api.context import ask_gemini
from app.system_prompt import system_prompt
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
    # data =redis_client.get("transcribe")
    # redis_client.flushdb()
    return {
        "status":"success",
        "message":"cache cleared",
        # "data":data
    }

@router.post("/ask_questions")
async def ask_questions(
    video_url:str,
    query:str
):
    """
    Accepts a transcript_id and a batch of questions, then returns answers processed asynchronously.
    """
    collection = chroma_client.get_collection(name=video_url)
    results = collection.query(
    query_texts=[query], # Chroma will embed this for you
    n_results=2 # how many results to return
    )
    answer = ask_gemini(system_prompt(query,results))
    return {"status":"success","data":answer}
    

@router.get("/status")
async def status():
    return {"status": "API is running"}

@router.get("/transcript_data")
async def get_transcript_data(video_url: str, query: str = None):
    """
    Retrieve the transcript data for the given video URL.
    Optionally, filter the results based on a search query.
    """
    
    collection = chroma_client.get_collection(name=video_url)
    results = collection.query(
    query_texts=[query], # Chroma will embed this for you
    n_results=2 # how many results to return
    )
    
    return {"status": "success", "data": results}


@router.get("/list_collections")
async def list_collections():
    """
    List all collections in the ChromaDB.
    """
    collections = chroma_client.list_collections()
    # Safely serialize each collection
    serialized_collections = []
    for col in collections:
        serialized_collections.append({
            "name": col.name,
            "id": col.id,
            "metadata": col.metadata,  # Or whatever properties you want
        })
    
    return {
        "status": "success",
        "data": serialized_collections
    }
