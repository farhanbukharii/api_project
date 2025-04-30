import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DEEPAI_API_KEY")

def generate_text(prompt: str):
    url = "https://api.deepai.org/api/text-generator"
    response = requests.post(
        url,
        data={'text': prompt},
        headers={'api-key': API_KEY}
    )
    try:
        result = response.json()
        print("🔍 DeepAI response:", result)

        # Navigate to output text
        output_obj = result.get("output")
        if isinstance(output_obj, dict):
            return output_obj.get("text")
        return None
    except Exception as e:
        print("❌ Error parsing DeepAI response:", e)
        return None
