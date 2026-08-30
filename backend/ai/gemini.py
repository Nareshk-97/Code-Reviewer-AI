from google import genai

from config import GEMINI_API_KEY


client = genai.Client(
    api_key=GEMINI_API_KEY
)


# Fast/current models
MODELS = [
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.7-flash"
]


def ask_gemini(prompt):

    last_error = None

    for model in MODELS:

        print(f"🤖 Trying Gemini model: {model}")

        try:

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            if response and response.text:

                print(
                    f"✅ Gemini success: {model}"
                )

                return response.text

            print(
                f"⚠️ {model} returned an empty response."
            )

        except Exception as err:

            last_error = err

            print(
                f"❌ {model} failed: {err}"
            )

            print(
                "⚡ Switching immediately to next model..."
            )

    print("❌ All Gemini models failed.")

    raise last_error