from dotenv import load_dotenv
import asyncio
import os

from litellm import acompletion
from src.tools import get_time_zone

load_dotenv(override=True)

async def test_get_response():
    user_message = "Hello, how are you?"
    messages = [{"content": user_message, "role": "user"}]
    response = await acompletion(model="openai/gpt-4o-mini", messages=messages)
    return response

def main():
    # openai_api_key = os.getenv("OPENAI_API_KEY")
    # if not openai_api_key:
    #     raise RuntimeError("OPENAI_API_KEY not set in environment")

    # # Just await the coroutine — do NOT use asyncio.run() here
    # response = await test_get_response()
    # # print(response)
    # print("\n=== Raw Response (Pretty JSON) ===\n")
    # print(response.choices[0].message.content)
    # print("\n==================================\n")
    get_time_zone('Tbilisi, Georgia')


if __name__ == "__main__":
    main()
