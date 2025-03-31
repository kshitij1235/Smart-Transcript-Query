from app.config import settings
from redis import Redis

# Connect to Redis
redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

# Check connection status
try:
    if redis_client.ping():
        print("Connected to Redis successfully!")
except Exception as e:
    print(f"Failed to connect to Redis: {e}")
