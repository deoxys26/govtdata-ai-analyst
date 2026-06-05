import os
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv


# Load .env from backend/.env
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=ENV_PATH)


def generate_explanation(question: str, intent: str, data):
    """
    Uses Gemini only to explain already-calculated analytics results.
    Pandas remains the source of truth.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API key is missing, so I can only return the calculated data without AI explanation."

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
You are an AI data analyst explaining government air quality data to a beginner.

User question:
{question}

Detected intent:
{intent}

Calculated result from pandas:
{data}

Rules:
- Do not invent numbers.
- Only use the calculated result given above.
- Explain in simple English.
- Mention that the data is from the EPA 2024 annual AQI county dataset.
- Keep the answer concise.
- If the result is a ranking, explain what the top result means.
"""

    response = model.generate_content(prompt)

    return response.text