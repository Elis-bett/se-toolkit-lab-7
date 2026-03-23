import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env.bot.secret")

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    LMS_API_BASE_URL = os.getenv("LMS_API_BASE_URL", "http://localhost:42002")
    LMS_API_KEY = os.getenv("LMS_API_KEY")
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    
    @classmethod
    def is_test_mode(cls):
        return cls.BOT_TOKEN is None
    
    @classmethod
    def validate(cls):
        """Validate required config."""
        if not cls.LMS_API_KEY:
            raise Exception("LMS_API_KEY not set in .env.bot.secret")
        if not cls.LMS_API_BASE_URL:
            raise Exception("LMS_API_BASE_URL not set in .env.bot.secret")
