# Load the environment variables from the .env file
from dotenv import load_dotenv
load_dotenv('ATT85165.env')

import os
key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

# import the required packages
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# create a DocumentAnalysisClient object
endpoint = "https://ocr-ie-hackathon.cognitiveservices.azure.com/"
client = DocumentAnalysisClient(endpoint, AzureKeyCredential(key))

# analyze a document from a local file
# invoice_url="https://www.invoicesimple.com/wp-content/uploads/2022/12/InvoiceSimple-PDF-Template.pdf"

file_path = "/Users/waterdamage123/Downloads/data_0611/XS2317910607.pdf"

with open(file_path, "rb") as f:
    poller = client.begin_analyze_document("prebuilt-document", f)
result = poller.result()

# print the extracted information
print(type(result))
