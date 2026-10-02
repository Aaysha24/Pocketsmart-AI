import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from dotenv import load_dotenv
from google import genai

from .auth import get_google_api_key
from .models import AIRequest, AIResponse


load_dotenv()

router = APIRouter()


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

TEMPLATES_DIR = os.path.join(
    BASE_DIR,
    "templates"
)


# =========================================================
# HOME PAGE
# =========================================================

@router.get(
    "/",
    response_class=HTMLResponse
)
async def home():

    template_path = os.path.join(
        TEMPLATES_DIR,
        "index.html"
    )

    try:

        with open(
            template_path,
            "r",
            encoding="utf-8"
        ) as file:

            html = file.read()

        return HTMLResponse(
            content=html
        )

    except FileNotFoundError:

        raise HTTPException(
            status_code=500,
            detail="templates/index.html file not found."
        )


# =========================================================
# AI GENERATE
# =========================================================

@router.post(
    "/generate",
    response_model=AIResponse
)
async def generate_ai(
    data: AIRequest
):

    api_key = get_google_api_key()

    if not api_key:

        raise HTTPException(
            status_code=500,
            detail=(
                "Google Gemini API key is missing. "
                "Please add GOOGLE_API_KEY to the .env file."
            )
        )


    try:

        client = genai.Client(
            api_key=api_key
        )


        model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        )


        prompt = f"""
You are Pocket smartAI,
a helpful and friendly AI assistant.

Give clear and useful answers.
Use simple language when possible.

Organize long answers with headings
or bullet points.

Do not invent facts.

If the user asks for code,
provide clean beginner-friendly code.

Keep the answer relevant to the user's question.

User's request:

{data.prompt}
"""


        interaction = client.interactions.create(

            model=model_name,

            input=prompt

        )


        result = interaction.output_text


        if not result:

            raise HTTPException(
                status_code=500,
                detail="Gemini returned an empty response."
            )


        return {
            "response": result
        }


    except HTTPException:

        raise


    except Exception as error:

        error_message = str(error)

        print(
            "Gemini Error:",
            repr(error)
        )


        if "503" in error_message:

            raise HTTPException(
                status_code=503,
                detail=(
                    "Gemini is temporarily busy. "
                    "Please try again after a short wait."
                )
            )


        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to generate AI response. "
                "Please check your Gemini API key "
                "and internet connection."
            )
        )