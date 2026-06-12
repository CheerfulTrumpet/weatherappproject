import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")

print(f"API Key: {api_key}")
print(f"Key length: {len(api_key) if api_key else 0}")

if api_key:
    # Test with simple location
    url = f"https://api.openweathermap.org/data/2.5/weather?q=London&appid={api_key}"
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
