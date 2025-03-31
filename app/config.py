import os
from dotenv import load_dotenv

class Settings:
    """Loads configuration values from the .env file."""

    def __init__(self, env_file=".env"):
        load_dotenv(env_file)  

        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

        self.REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
        self.REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
        self.REDIS_DB = int(os.getenv("REDIS_DB", 0))

        self.DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

    def get_redis_config(self):
        return {
            "host": self.REDIS_HOST,
            "port": self.REDIS_PORT,
            "db": self.REDIS_DB,
        }

settings = Settings()