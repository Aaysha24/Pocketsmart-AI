import os

from dotenv import load_dotenv


load_dotenv()


def get_google_api_key() -> str:
    """Get Google Gemini API key from .env."""

    return os.getenv(
        "GOOGLE_API_KEY",
        ""
    ).strip()


def is_google_api_key_configured() -> bool:
    """Check whether the API key is configured."""

    return bool(
        get_google_api_key()
    )