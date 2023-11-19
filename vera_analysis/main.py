
from datetime import datetime, timedelta
import os
import json
import argparse


from column_processors.isin import get_isin
from column_processors.issuer import get_issuer
from column_processors.name import get_name
from column_processors.underlyings import get_underlyings
from column_processors.currency import get_currency
from column_processors.strike import get_strike
from column_processors.launch_date import get_launch_date
from column_processors.final_valuation_date import get_final_valuation_date
from column_processors.maturity import get_maturity
from column_processors.cap import get_cap
from column_processors.barrier import get_barrier



# ok we need a main function which handles the main process pipeline
def process_single_doc(doc_name:str) -> None:
    """
    Given a document, we split the processing step into several columns
    :param doc_name:
    :return:
    """
    isin = get_isin(doc_name)
    issuer = get_issuer(doc_name)
    name = get_name(doc_name)
    underlyings = get_underlyings(doc_name)
    currency = get_currency(doc_name)
    strike = get_strike(doc_name)
    launch_date = get_launch_date(doc_name)
    final_valuation_date = get_final_valuation_date(doc_name)
    maturity = get_maturity(doc_name)
    cap = get_cap(doc_name)
    barrier = get_barrier(doc_name)

    # we generate a row of data to save to the csv file
    row = {
        'isin': isin,
        'issuer': issuer,
        'name': name,
        'underlyings': underlyings,
        'currency': currency,
        'strike': strike,
        'launch_date': launch_date,
        'final_valuation_date': final_valuation_date,
        'maturity': maturity,
        'cap': cap,
        'barrier': barrier
    }



    return






if __name__ == '__main__':
    # args parsing
    parser = argparse.ArgumentParser(description='Process some integers.')
    # folder of the pdfs
    parser.add_argument('--pdfs-folder', type=str, default='pdfs', help='folder of the pdfs')
    #folder of the
