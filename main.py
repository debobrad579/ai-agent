import os
from dotenv import load_dotenv
from google.genai import Client, types
import sys
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

FUNCTIONS = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = Client(api_key=api_key)


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name not in FUNCTIONS:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": FUNCTIONS[function_call_part.name]("./calculator", **function_call_part.args)},
            )
        ],
    )


def main():
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    user_prompt = sys.argv[1]
    verbose = True if len(sys.argv) > 2 and sys.argv[2] == "--verbose" else False

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for _ in range(20):
        res = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[types.Tool(
                    function_declarations=[
                        schema_get_files_info,
                        schema_get_file_content,
                        schema_write_file,
                        schema_run_python_file,
                    ]
                )],
                system_instruction=system_prompt,
            ),
        )

        if not res.function_calls:
            print(res.text)
            break

        if res.candidates:
            for candidate in res.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        if res.function_calls:
            call_res = call_function(res.function_calls[0], verbose)
            try:
                func_res = call_res.parts[0].function_response.response
                messages.append(call_res)
                if verbose:
                    print(func_res)
            except Exception:
                raise Exception("Error: An error has occured when calling function.")

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {res.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
