from app.api.dependency import get_chunked_transcript, get_youtube_transcript
import json
from app.dependency import Summarizer_log
from app.database import chroma_client

class BatchProcessing:
    def __init__(self, video_url: str) -> None:
        self.video_url = video_url
        self.query = get_youtube_transcript(self.video_url)
        video_id = video_url.split("v=")[-1].split("&")[0]
        self.collection = chroma_client.create_collection(name=video_id)
        print(chroma_client.list_collections())

    def clean_transcript(self, script):
        """Removes unnecessary words, filler content, and repeating words."""

        if script.get("t"):
            for word in ["um", "uh", "you know", "like", "so", "okay", "alright", "[Applause]", "[Music]","[ __ ]"]:
                script["t"] = script["t"].replace(word, "")
            script["t"] = self.remove_repeating_words(script["t"])
            script["t"] = " ".join(script["t"].split())


    def remove_repeating_words(self, text, window=5):
        words = text.split()
        result = []
        recent_words = []
    
        for word in words:
            if word.lower() not in recent_words:
                result.append(word)

            recent_words.append(word.lower())
            if len(recent_words) > window:
                recent_words.pop(0)

        return ' '.join(result)

    def process_query(self):
        """Filters and trims the transcript until it meets the requirements."""
        
        if self.query[0].get("error"):
            return None 
    
        # Clean the transcript
        for lines in self.query:
            self.clean_transcript(lines)

        # Save to ChromaDB
        summary = Summarizer_log(self.query,self.collection).pipeline()

        return summary
        