# Student Setup Instructions for the AI Hackathon  

Students should create a directory and copy files .env and .gitignore in it. Notice that .gitignore is required to avoid API keys from being committed to source control platforms such as GitHub.  
Then, create a Python environment with at least the following requirements:

```
openai 
python-dotenv 
azure-ai-formrecognizer==3.2.0
```  

For example, you can use these commands on a Linux OS, which assumes a recent Python3 local installation is available:

```
# Create a virtual environment named aihackathon
python3 -m venv aihackathon

# Activate the virtual environment
source aihackathon/bin/activate

# Install the required packages
pip install openai python-dotenv azure-ai-formrecognizer==3.2.0
```

## Test OpenAI access  


```
# Load the environment variables from the .env file
from dotenv import load_dotenv
load_dotenv()  

# import the required packages
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant for university students."},
    {"role": "user", "content": "Why should I join IE University's AI Hackathon?"}
  ],
  temperature=0.7
)

print(response.choices[0].message.content)
```

## Test Azure Document Intelligence Service

```
# Load the environment variables from the .env file
from dotenv import load_dotenv
load_dotenv()

import os
key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

# import the required packages
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# create a DocumentAnalysisClient object
endpoint = "https://ocr-ie-hackathon.cognitiveservices.azure.com/"
client = DocumentAnalysisClient(endpoint, AzureKeyCredential(key))

# analyze a document from a local file
invoice_url="https://www.invoicesimple.com/wp-content/uploads/2022/12/InvoiceSimple-PDF-Template.pdf"
with open(file_path, "rb") as f:
    poller = client.begin_analyze_document_from_url("prebuilt-invoice", invoice_url)
result = poller.result()

# print the extracted information
result
```