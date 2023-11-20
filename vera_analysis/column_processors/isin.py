import json as json
import re


def get_isin(document_path: str) -> str:
    # do a regex function
    # load the json based on the document path
    # regex through the json to find the isin
    # first check the keys of the json
    # load
    import pdb;
    pdb.set_trace()
    # read a json file
    with open(document_path, 'r') as f:
        json_doc = json.load(f)
    # regex
    # return the isin
    # ISIN pattern \b[A-Z]{2}[A-Z0-9]{9}\d\b

    isin_matches = re.findall(r'\b[A-Z]{2}[A-Z0-9]{9}\d\b', str(json_doc))
    if isin_matches:
        # Take the first match if there are multiple
        isin = isin_matches[0]
    return isin


"""
    # ISIN pattern \b[A-Z]{2}[A-Z0-9]{9}\d\b 

    Country Code: 
    The first two characters are letters representing the country code based on the ISO 3166-1 alpha-2 standard. 
    This code identifies the country of issue for the security. 
    It doesn't necessarily indicate the country where the security is traded.

    National Security Identifier: The next nine characters (which can be both letters and numbers) are the national 
    security identifier, assigned by a national numbering agency of the respective country. 
    This part of the ISIN varies from one country to another in format and structure.

    Check Digit: The last character is a check digit calculated using the MOD 11-2 algorithm. 
    This digit is used to verify the validity of the ISIN.

"""