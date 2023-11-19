import json as json
import re


def get_isin(document_path:str) -> str:
    # do a regex function
    # load the json based on the document path
    # regex through the json to find the isin
    # first check the keys of the json

    # load
    json_doc = json.load(document_path)
    # regex
    # return the isin
    # ISIN pattern \b[A-Z]{2}[A-Z0-9]{9}\d\b
    isin = re.search(r'\b[A-Z]{2}[A-Z0-9]{9}\d\b', json_doc)
    if len(isin) > 1:
        # take the first one
        isin = isin[0]
    return isin