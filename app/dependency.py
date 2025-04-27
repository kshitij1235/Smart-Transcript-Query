import chromadb
from transformers import pipeline
import torch
import uuid  # for generating unique IDs

class Summarizer_log:
    def __init__(self, text: list, collection):
        """
        text: list of dicts with keys 's' (timestamp) and 't' (text)
        collection: an existing chromadb collection
        """
        self.text = text
        self.client = chromadb.Client()
        self.collection = collection

        # Load the summarization pipeline
        device = 0 if torch.cuda.is_available() else -1
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)

    def summarize_chunk(self, chunk, max_len=100, min_len=30):
        try:
            if len(chunk) > 4000:
                chunk = chunk[:4000]
            result = self.summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)
            return result[0]["summary_text"]
        except Exception as e:
            print(f"Summarization failed: {e}")
            return None

    def pipeline(self):
        if not self.text:
            return "No valid content to process."

        # Combine entries into a big block with timestamps for smarter chunking
        combined_blocks = []
        current_block = ""
        current_timestamps = []

        for entry in self.text:
            timestamp = entry.get("s")
            content = entry.get("t", "").strip()

            if not content:
                continue

            if len(current_block) + len(content) < 2000:
                current_block += " " + content
                current_timestamps.append(timestamp)
            else:
                combined_blocks.append((current_block.strip(), current_timestamps))
                current_block = content
                current_timestamps = [timestamp]

        if current_block:
            combined_blocks.append((current_block.strip(), current_timestamps))

        print(f"Total combined blocks: {len(combined_blocks)}")

        # Summarize each block and store the summary with the *first timestamp*
        for i, (block, timestamps) in enumerate(combined_blocks):
            summary = self.summarize_chunk(block)
            if summary:
                first_timestamp = timestamps[0] if timestamps else f"chunk-{i}"
                doc_id = str(uuid.uuid4())
                self.collection.add(
                    documents=[summary],
                    metadatas=[{"timestamp": first_timestamp, "type": "summary"}],
                    ids=[doc_id]
                )
                print(f"[✔] Stored summary at {first_timestamp}")
            else:
                print(f"[✘] Skipped block {i+1}")

        return "Summarization and storage complete."
