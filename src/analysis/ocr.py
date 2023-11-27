from dotenv import load_dotenv

load_dotenv()
# import the required packages
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from column_processors.helpers.create_logger import create_logger
import os
import json

LOG = create_logger()

# create a DocumentAnalysisClient object
endpoint = "https://ocr-ie-hackathon.cognitiveservices.azure.com/"


def perform_ocr(pdfs_folder: str, OCR_destinationfile_name: str) -> str:
    """
    parses pdf files in given directory with Azure OCR and returns the filepath of the directory the json outputs were saved in.
    """

    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    client = DocumentAnalysisClient(endpoint, AzureKeyCredential(key))

    # Create output directory if it doesn't exist
    json_output_dir_fp = os.path.join(pdfs_folder, OCR_destinationfile_name)

    if not os.path.exists(json_output_dir_fp):
        os.mkdir(json_output_dir_fp)

    # Only consider .pdf files for parsing
    term_sheets = [
        i for i in os.listdir(pdfs_folder) if os.path.splitext(i)[-1].lower() == ".pdf"
    ]

    # Iterate over the Term Sheets in the data directory
    for filename in term_sheets:
        LOG.info(f"Parsing {filename} with Azure OCR")

        filepath = os.path.join(pdfs_folder, filename)
        # Parse the document with azure OCR
        with open(filepath, "rb") as f:
            poller = client.begin_analyze_document("prebuilt-document", f)
        result = poller.result()

        dict_result = result.to_dict()

        items_dict = {}
        # Parsing the key-value-pairs dict in the results for easier access to items
        for i in dict_result["key_value_pairs"]:
            key = i["key"]["content"].replace("\n", " ")

            try:
                value = i["value"]["content"]
            except TypeError:
                value = None

            confidence = i["confidence"]
            # New dict only includes the key, value, and confidence values for each item in result dict
            items_dict[key] = value, confidence

        # Output dictionary
        document_dict = {
            "key-value_pairs": items_dict,
            "full_text": dict_result["content"],
        }

        output_filename = ".".join(filename.split(".")[:-1]) + ".json"
        json_output_filepath = os.path.join(json_output_dir_fp, output_filename)
        # Saving to json

        with open(json_output_filepath, "w") as f:
            json.dump(document_dict, f)

    return json_output_dir_fp


def create_json_saving_dir(dir_path: str) -> str:
    """
    Checks if dir path exists and modifies until successful creation of new dir.
    """
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        i = 0
        dir_path = dir_path + f"({i})"
        while True:
            try:
                os.mkdir(dir_path)
            except FileExistsError:
                dir_path = "".join(dir_path.split("(")[:-1]) + f"({i})"
                i += 1
                continue
            break
