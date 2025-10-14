import os
import google.generativeai as genai
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
# Configure the Gemini API key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
# Create a Gemini Pro model
model = genai.GenerativeModel('gemini-2.5-flash')
# The prompt you want to send to the model
prompt = "Write a short, encouraging poem about learning to code."
print(f"Sending prompt: '{prompt}'")
# Generate content
response = model.generate_content(prompt)
# Print the response from the model
print("\n--- Gemini's Response ---")
print(response.text)
print("------------------------")