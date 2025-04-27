# from redis import Redis
import chromadb

from chromadb import PersistentClient

chroma_client = PersistentClient(path="./chroma_storage")
