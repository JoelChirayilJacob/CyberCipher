import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Testing simple API call...")

try:
    # Test without JSON mode first
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say 'Hello, API works!' in 3 words or less."
    )
    
    print(f"✅ Success! Response: {response.text}")
    
except Exception as e:
    print(f"❌ Failed: {e}")
