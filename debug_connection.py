import os
import httpx
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")

def test_raw_connection():
    print("--- Detailed Connection Debug ---")
    url = "https://integrate.api.nvidia.com/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        # We use a 30s timeout and a direct GET request
        with httpx.Client(timeout=30.0) as client:
            print(f"Connecting to {url}...")
            response = client.get(url, headers=headers)
            print(f"Status Code: {response.status_code}")
            print("Successfully reached NVIDIA NIM!")
            
    except httpx.ConnectTimeout:
        print("❌ Error: Connection Timed Out. Your network cannot reach the server.")
    except httpx.ProxyError:
        print("❌ Error: Proxy issue detected.")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    test_raw_connection()