import os
from dotenv import load_dotenv

load_dotenv(".env.bot.secret")


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    LMS_API_BASE_URL = os.getenv("LMS_API_BASE_URL", "https://lms.example.com/api")
    LMS_API_KEY = os.getenv("LMS_API_KEY")
    LLM_API_KEY = os.getenv("LLM_API_KEY")

    @classmethod
    def is_test_mode(cls):
        return cls.BOT_TOKEN is None
