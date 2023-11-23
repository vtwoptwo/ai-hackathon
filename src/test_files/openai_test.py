# Load the environment variables from the .env file
from dotenv import load_dotenv
load_dotenv('ATT85165.env')

import os

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
print(OPENAI_API_KEY)

# import the required packages
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)
response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant for university students."},
    {"role": "user", "content": "Why should I join IE University's AI Hackathon?"}
  ],
  temperature=0.7
)

print(response.choices[0].message.content)
