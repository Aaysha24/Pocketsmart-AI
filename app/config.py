from pathlib import Path

from dotenv import load_dotenv
import os


# Project base folder
BASE_DIR = Path(
    __file__
).resolve().parent.parent


# Load .env file
load_dotenv(
    BASE_DIR / ".env"
)


# Application name
APP_NAME = os.getenv(
    "APP_NAME",
    "Pocket smartAI"
)


# Google Gemini API key
GOOGLE_API_KEY = os.getenv(
    "GOOGLE_API_KEY",
    ""
)


# Gemini model
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)