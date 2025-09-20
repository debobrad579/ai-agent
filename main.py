import os
from dotenv import load_dotenv
from google.genai import Client, types
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = Client(api_key=api_key)



def main():
    user_prompt = sys.argv[1]
    verbose = True if len(sys.argv) > 2 and sys.argv[2] == "--verbose" else False

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )

    print(res.text)

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {res.usage_metadata.candidates_token_count}")



if __name__ == "__main__":
    main()
