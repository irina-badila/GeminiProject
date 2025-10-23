from http import client
import os
import sys
#import google.generativeai as generai
from dotenv import load_dotenv
from google.genai import types
from google import genai
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_files_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

def main():
    #print("Hello from geminiproject!")
    # Load environment variables from .env file
    load_dotenv()
    # Configure the Gemini API key
    api_key = os.getenv("GOOGLE_API_KEY")
    #generai.configure(api_key=api_key)
    client = genai.Client(api_key=api_key)

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    if not args:
        print("AI Code Assistant")
        print('\nUsage:python main.py "Your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    user_prompt = " ".join(args)
    print(f"User prompt:{user_prompt}\n")

    messages = [types.Content(role='user', parts=[types.Part(text=user_prompt)]),]
    available_functions = types.Tool(
                        function_declarations=[
                        schema_get_files_info, 
                        schema_get_files_content, 
                        schema_write_file, 
                        schema_run_python_file,]
    )
    config = types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    model = "gemini-2.5-flash"
    response = client.models.generate_content(model = model,
                                              contents=messages,
                                              config=config)
    if response is None or response.usage_metadata is None:
        print("No response from the model.")
        return
    # Print the response from the model
    if verbose:
        print("User prompt:", user_prompt)
        print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name} with arguments: {function_call.args}")
    else:
        print("Response:")
        print(response.text)


if __name__ == "__main__":
    main()