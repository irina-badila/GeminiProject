# Import necessary libraries
from http import client
import os # Used for accessing environment variables and system paths
import sys # Used for accessing command-line arguments (sys.argv)
#import google.generativeai as generai
from dotenv import load_dotenv # Used to load variables from a .env file (like API keys)
from google.genai import types # Specific types for configuring the Gemini API
from google import genai # The main Google Gemini API client library
from prompts import system_prompt # Imports a custom system instruction/prompt from a local file
from functions.get_files_info import schema_get_files_info # Imports the *schema* (definition) for a function to list files
from functions.get_file_content import schema_get_files_content # Imports the schema for a function to read files
from functions.write_file import schema_write_file # Imports the schema for a function to write files
from functions.run_python_file import schema_run_python_file # Imports the schema for a function to run Python code
from call_function import call_function # Imports a custom helper function that actually *executes* the function calls
from config import MAX_ITERATIONS # Imports a constant defining the maximum number of loops

def main():
    #print("Hello from geminiproject!")

    # Load environment variables from .env file
    load_dotenv()

    # Configure the Gemini API key
    api_key = os.getenv("GOOGLE_API_KEY")

    #generai.configure(api_key=api_key)
    # Initialize the Gemini client with the loaded API key
    client = genai.Client(api_key=api_key)

    # --- Argument Parsing ---
    # Check if '--verbose' flag is present in the command-line arguments
    verbose = "--verbose" in sys.argv

    # Collect all command-line arguments that are *not* flags (don't start with '--')
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    # If no arguments were provided, print usage instructions and exit
    if not args:
        print("AI Code Assistant")
        print('\nUsage:python main.py "Your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    # Join all collected arguments into a single string to form the user's prompt
    user_prompt = " ".join(args)
    print(f"User prompt:{user_prompt}\n") # Print the user's prompt to the console


    # --- API Configuration ---
    
    # Initialize the message history with the user's first prompt
    messages = [types.Content(role='user', parts=[types.Part(text=user_prompt)]),]

    # Define the set of tools (functions) the AI model is allowed to use
    available_functions = types.Tool(
                        function_declarations=[
                        schema_get_files_info, 
                        schema_get_files_content, 
                        schema_write_file, 
                        schema_run_python_file,]
    )

    # Set the configuration for the API call
    config = types.GenerateContentConfig(
                                        tools=[available_functions], # Tell the model which tools it can call
                                        system_instruction=system_prompt) # Provide the system-level instructions (e.g., "You are a helpful assistant")
    
    # Specify which model to use
    model = "gemini-2.5-flash"

    # --- Main Execution Loop ---
    # Loop for a maximum number of iterations to prevent infinite loops
    for i in range(MAX_ITERATIONS):
        # Send the entire conversation history and configuration to the model
        response = client.models.generate_content(model = model,
                                                contents=messages,
                                                config=config)
        
        # Handle cases where the model doesn't return a valid response
        if response is None or response.usage_metadata is None:
            print("No response from the model.")
            return
        
        # If in verbose mode, print token usage details
        if verbose:
            print("User prompt:", user_prompt)
            print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        # Process the model's response
        if response.candidates:
            for candidate in response.candidates:
                # Get the model's reply (which could be text or a function call)
                function_call_content = candidate.content
                # Add the model's reply to the conversation history
                messages.append(function_call_content)

        # --- Function Calling Logic ---
        
        # Check if the model's response *was* a function call
        # If not, it means the model gave a final text answer
        if not response.function_calls:
            return response.text

        # If we are here, the model *did* request a function call
        function_responses = []# A list to hold the *results* of the function calls

        # Iterate through each function call requested by the model
        for function_call_part in response.function_calls:
            # Execute the function using the helper
            function_call_result = call_function(function_call_part, verbose)
            
            # Basic error checking for the function result
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception("empty function call result")
            
            # If verbose, print the *result* of the function call
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            
            # Add the function's *result* to our list
            function_responses.append(function_call_result.parts[0])

        if not function_responses:
            raise Exception("no function responses generated, exiting.")
        
        # Add all function results to the conversation history
        # The role is 'user' here, but it's *content* is a function response.
        # This tells the model "Here is the result of the function you asked me to run."
        messages.append(types.Content(role="user", parts=function_responses))

if __name__ == "__main__":
    main()