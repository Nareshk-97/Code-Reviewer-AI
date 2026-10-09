from google import genai
from google.genai import types

from config import GEMINI_API_KEY


TIMEOUT_MS = 10_000

client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(
        timeout=TIMEOUT_MS
    )
)


MODELS = [
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.7-flash"
]


class GeminiReviewError(Exception):
    """Custom exception for Gemini review failures."""
    pass


def ask_gemini(prompt):
    """
    Generate a code review using Gemini.

    Each model has a 10-second request timeout.
    If one model fails or times out, the next model is tried.
    """

    if not prompt or not prompt.strip():
        raise GeminiReviewError(
            "Gemini prompt cannot be empty."
        )

    if not GEMINI_API_KEY:
        raise GeminiReviewError(
            "Gemini API key is not configured."
        )

    last_error = None

    for model in MODELS:

        print(f"Trying Gemini model: {model}")

        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            if response and response.text:
                print(f"Gemini success: {model}")
                return response.text

            print(f"{model} returned an empty response.")

            last_error = GeminiReviewError(
                f"{model} returned an empty response."
            )

        except Exception as err:

            last_error = err

            print(f"Gemini model failed: {err}")
            print("Switching to next Gemini model...")

    print("All Gemini models failed.")

    raise GeminiReviewError(
        "Gemini AI service is currently unavailable."
    ) from last_error