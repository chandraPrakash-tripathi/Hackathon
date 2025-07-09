import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_query_insights(df, savings):
    top = df[['USER_NAME', 'DURATION_SEC', 'CREDITS_USED_CLOUD_SERVICES']].head().to_string()
    prompt = f"""
    Here is Snowflake query history data:\n{top}
    
    Estimated cost savings (based on idle warehouses + optimization): ${savings}
    
    Provide 3 actionable insights to reduce compute cost and improve performance.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content
