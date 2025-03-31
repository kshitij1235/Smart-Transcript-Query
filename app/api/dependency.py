import requests
from youtube_transcript_api import YouTubeTranscriptApi
import datetime

def generate_content(prompt: str):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={settings.GEMINI_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}

def get_youtube_transcript(video_url):
    """Fetches transcript and timestamps from a YouTube video URL."""
    video_id = video_url.split("v=")[-1].split("&")[0]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_data = []
        
        for entry in transcript:
            transcript_data.append({"timestamps": format_timestamp(entry['start']), "line": entry["text"]})
        
        return transcript_data
    
    except Exception as e:
        return {"error": str(e)}

def format_timestamp(seconds):
    return str(datetime.timedelta(seconds=int(seconds))).zfill(8)

def get_chunked_transcript(video_url, chunk_duration=300): 
    """Splits a YouTube transcript into chunks based on timestamps."""
    transcript_data = get_youtube_transcript(video_url,)

    if "error" in transcript_data:
        return transcript_data

    chunks = []
    current_chunk = {"start": 0, "end": 0, "text": ""}
    for entry in transcript_data:
        start_seconds = datetime.timedelta(hours=int(entry['timestamps'][:2]), minutes=int(entry['timestamps'][3:5]), seconds=int(entry['timestamps'][6:8])).total_seconds()
        if current_chunk["end"] == 0:
            current_chunk["end"] = start_seconds + chunk_duration

        if start_seconds < current_chunk["end"]:
            current_chunk["text"] += entry["line"] + " "
        else:
            chunks.append(current_chunk)
            current_chunk = {"start": current_chunk["end"], "end": current_chunk["end"] + chunk_duration, "text": entry["line"] + " "}
    chunks.append(current_chunk) #append the last chunk.
    return chunks
