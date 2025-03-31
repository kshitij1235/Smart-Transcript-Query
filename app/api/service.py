from app.api.dependency import get_chunked_transcript
from app.database import redis_client
import json
class BatchProcessing:
    def __init__(self, video_url: str) -> None:
        self.video_url = video_url
        self.query = get_chunked_transcript(self.video_url)

    def clean_transcript(self, script):
        """Removes unnecessary words, filler content, and repeating words."""
        
        if "text" in script:
            for word in ["um", "uh", "you know", "like", "so", "okay", "alright", "[Applause]", "[Music]"]:
                script["text"] = script["text"].replace(word, "")
                script["text"] = self.remove_repeating_words(script["text"])
            script["text"] = " ".join(script["text"].split())

    def remove_repeating_words(seld , text, window=5):
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
        

        if self.query.get("error"):
            return None 
        
        for query in self.query:
            self.clean_transcript(query)
        
        redis_client.set("transcribe", json.dumps(self.query))
        return self.query