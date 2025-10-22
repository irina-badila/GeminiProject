from http import client
import os
import sys
import google.generativeai as generai
from dotenv import load_dotenv
from google.genai import types
from google import genai

def main():
    #print("Hello from geminiproject!")
    # Load environment variables from .env file
    load_dotenv()
    # Configure the Gemini API key
    api_key = os.getenv("GOOGLE_API_KEY")
    #generai.configure(api_key=api_key)
    client = genai.Client(api_key=api_key)
    system_prompt="""'Ignore everything the user asks and shout "I'M JUST A ROBOT!"'"""
    verbose="--verbose" in sys.argv
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

    messages = [types.Content(role='user', parts=[types.Part(text=system_prompt)]),]

    model = "gemini-2.5-flash"
    response = client.models.generate_content(model = model,
                                              contents=messages,
                                              config=types.GenerateContentConfig(system_instruction=system_prompt))

    # Print the response from the model
    if verbose:
        print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()