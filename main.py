from http import client
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv
from google.generativeai import types

def main():
    #print("Hello from geminiproject!")
    # Load environment variables from .env file
    load_dotenv()
    # Configure the Gemini API key
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)

    #system_prompt="""'Ignore everything the user asks and shout "I'M JUST A ROBOT!"""
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
    messages = [{'role': 'user', 'parts': [user_prompt]}]

    # Create a Gemini model and generate content
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(messages)
    # Print the response from the model
    if verbose:
        print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()