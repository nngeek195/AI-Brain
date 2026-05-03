import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=os.getenv("NVIDIA_API_KEY"))

print("Testing connection...")
try:
    # Use a faster, non-reasoning model for the test
    response = client.chat.completions.create(
        model="meta/llama-3.1-8b-instruct", 
        messages=[{"role": "user", "content": "hello"}],
        timeout=10.0
    )
    print(f"Success! Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"Connection Failed: {e}")