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
from call_function import call_function
from config import MAX_ITERATIONS

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

    #do a maximum of 20 iterations for fixing the calculator
    for i in range(MAX_ITERATIONS):
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

        if response.candidates:
            for candidate in response.candidates:
                function_call_content = candidate.content
                messages.append(function_call_content)

        if not response.function_calls:
            return response.text

        function_responses = []
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception("empty function call result")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])

        if not function_responses:
            raise Exception("no function responses generated, exiting.")
        messages.append(types.Content(role="user", parts=function_responses))

if __name__ == "__main__":
    main()