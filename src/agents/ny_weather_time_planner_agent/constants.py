from dotenv import load_dotenv
import os

APP_NAME = "weather_app"
USER_ID = "1234"
SESSION_ID = "session1234"

load_dotenv(override=True)

LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")