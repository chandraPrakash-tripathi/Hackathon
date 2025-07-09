import os
import requests
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

def generate_query_insights(df: pd.DataFrame, savings: float) -> str:
    prompt = f"""
    Analyze the following Snowflake query data:
    {df[['USER_NAME', 'DURATION_SEC', 'CREDITS_USED_CLOUD_SERVICES']].head().to_string(index=False)}

    Estimated cost savings: ${savings:.2f}

    Give 3 detailed insights to reduce compute usage and optimize performance.
    """

    payload = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "top_p": 1,
        "max_tokens": 512,
        "stream": False,
    }

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"
