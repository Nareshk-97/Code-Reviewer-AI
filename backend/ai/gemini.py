from google import genai

from config import GEMINI_API_KEY


# ==========================================
# GEMINI CLIENT
# ==========================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ==========================================
# GEMINI MODEL FALLBACKS
# ==========================================

MODELS = [
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.7-flash"
]


# ==========================================
# CUSTOM GEMINI ERROR
# ==========================================

class GeminiReviewError(Exception):
    """
    Custom exception for Gemini review failures.
    """
    pass


# ==========================================
# ASK GEMINI
# ==========================================

def ask_gemini(prompt):

    if not prompt or not prompt.strip():
        raise GeminiReviewError(
            "Gemini prompt cannot be empty."
        )

    if not GEMINI_API_KEY:
        raise GeminiReviewError(
            "Gemini API key is not configured."
        )

    last_error = None

    # Try each Gemini model
    for model in MODELS:

        print(
            f"🤖 Trying Gemini model: {model}"
        )

        try:

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            # Check response
            if response and response.text:

                print(
                    f"✅ Gemini success: {model}"
                )

                return response.text

            # Empty response
            print(
                f"⚠️ {model} returned an empty response."
            )

            last_error = GeminiReviewError(
                f"{model} returned an empty response."
            )

        except Exception as err:

            last_error = err

            print(
                f"❌ {model} failed: {err}"
            )

            print(
                "⚡ Switching to next Gemini model..."
            )

    # ==========================================
    # ALL MODELS FAILED
    # ==========================================

    print(
        "❌ All Gemini models failed."
    )

    raise GeminiReviewError(
        "Gemini AI service is currently unavailable."
    ) from last_error