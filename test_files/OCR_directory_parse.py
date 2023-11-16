from dotenv import load_dotenv
load_dotenv()

import os
key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

# import the required packages
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

import json

from sys import argv
data_dir_fp = argv[1]

# create a DocumentAnalysisClient object
endpoint = "https://ocr-ie-hackathon.cognitiveservices.azure.com/"
client = DocumentAnalysisClient(endpoint, AzureKeyCredential(key))

output_dir_fp = os.path.join(data_dir_fp, 'OCR_output')

# Create output directory if it doesn't exist
try:
    os.mkdir(output_dir_fp)
except FileExistsError:
    pass

# Only consider .pdf files for parsing
term_sheets = [i for i in os.listdir(data_dir_fp) if os.path.splitext(i)[-1].lower() == '.pdf']

# Iterate over the Term Sheets in the data directory
for filename in term_sheets:

    print(f"Parsing {filename}")

    filepath = os.path.join(data_dir_fp, filename)

    # Parse the document with azure OCR
    with open(filepath, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-document", f)
    result = poller.result()

    dict_result = result.to_dict()


    items_dict = {}
    # Parsing the key-value-pairs dict in the results for easier access to items
    for i in dict_result['key_value_pairs']:

        key = i['key']['content'].replace('\n',' ')

        try:
            value = i['value']['content']
        except TypeError:
            value = None

        confidence = i['confidence']

        items_dict[key] = value, confidence # New dict only includes the key, value, and confidence values for each item in result dict

    # Output dictionary
    document_dict = {'key-value_pairs':items_dict,
                    'full_text':dict_result['content']}

    output_filename = '.'.join(filename.split('.')[:-1])+'.json'
    output_filepath = os.path.join(output_dir_fp, output_filename)
    # Saving to json
    with open(output_filepath, 'w') as f:

        json.dump(document_dict, f)
