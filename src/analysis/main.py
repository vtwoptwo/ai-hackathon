from datetime import datetime, timedelta
import os
import json
import argparse
from typing import List
import pandas as pd
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
from column_processors.helpers.create_logger import create_logger
from column_processors.helpers.utils import retry_on_rate_limit_error
from dataclasses import dataclass

LOG = create_logger()
@dataclass
class row:
    name: str
    isin: str
    issuer: str
    underlyings: List[str]
    currency: str
    strike: List[str]
    launch_date: str
    final_valuation_date: str
    maturity: str
    cap: str
    barrier: str



def process_single_doc(doc_name: str, folder_path:str) -> None:
    """
    Given a document, we split the processing step into several columns
    :param doc_name:
    :return:
    """
    full_path = folder_path + '/' + doc_name
    LOG.info(f"Starting Pipeline for {doc_name}")

    #name
    LOG.info("Processing Name")
    name = get_name(doc_name)
    LOG.info(f"Processed name {name}")

    #isin
    LOG.info("Processing isin")
    isin = get_isin(document_path=full_path)
    LOG.info(f"Processed isin: {isin}")

    #issuer
    LOG.info("Processing issuer")
    issuer = get_issuer(document_path=full_path)
    LOG.info(f"Processed issuer:{issuer}")

    #underlyings
    LOG.info("Processing underlyings")
    underlyings = get_underlyings(document_path=full_path)
    LOG.info(f"Processed underlyings: {underlyings}")

    LOG.info("Processing currency")
    currency = get_currency(document_path=full_path)
    LOG.info(f"Processed currency: {currency}")

    LOG.info("Processing strike")
    strike = get_strike(full_path)
    LOG.info(f"Processed strike: {strike}")

    LOG.info("Processing launch date")
    launch_date = get_launch_date(full_path)
    LOG.info(f"Processed launch_date: {launch_date}")

    LOG.info("Processing final valuation date")
    final_valuation_date = get_final_valuation_date(full_path)
    LOG.info(f"Processed final_valuation date: {final_valuation_date}")

    LOG.info("Processing Maturity")
    maturity = get_maturity(full_path)
    LOG.info(f"Processed Maturity: {maturity}")

    LOG.info("Processing cap")
    cap = get_cap(document_name=full_path)
    LOG.info(f"Processed cap: {cap}")

    LOG.info("Processing barrier")
    barrier = get_barrier(document_name=full_path)
    LOG.info(f"Processed barrier: barrier")

    max = 5
    count = 0
    while len(underlyings) != len(strike) and count <= max:
        LOG.info("Retrying underlyings and strike: {count}")
        underlyings = get_underlyings(document_path=full_path)
        strike = get_strike(full_path)
        count += 1


    final_output = row(name=name, isin=isin,
                       issuer=issuer,
                       underlyings=underlyings,
                       currency=currency,
                       strike=strike,
                       launch_date=launch_date,
                       final_valuation_date=final_valuation_date,
                       maturity=maturity,
                       cap=cap,
                       barrier=barrier)

    LOG.info(f'Processed {doc_name} with row {final_output}')

    row_final = {'name': final_output.name,
                    'isin': final_output.isin,
                    'issuer': final_output.issuer,
                    'underlyings': final_output.underlyings,
                    'currency': final_output.currency,
                    'strike': final_output.strike,
                    'launch_date': final_output.launch_date,
                    'final_valuation_date': final_output.final_valuation_date,
                    'maturity': final_output.maturity,
                    'cap': final_output.cap,
                    'barrier': final_output.barrier}
    return row_final


def generate_pipeline_for_files_in_general_folder(path_to_root_folder: str) -> None:
    path_to_root_folder = os.path.abspath(path_to_root_folder)
    LOG.info(f'Processing files in {path_to_root_folder}')
    # get current path
    # we need to get the list of files in the folder
    files_in_folder = os.listdir(path_to_root_folder+'/')
    # here we have an intermediate step missing which is the ocr of the files, for now to be able to focus on the extraciton of data given a json output,
    # we will assume that the ocr has been done and we have a json file for each pdf
    # have the pdfs in the same folder as the json files. The only difference is the extension
    # TODO: bring in the intermediate step of OCR which is (1. take a pdf, 2. ocr it, 3. save the json output into desired folder)

    json_files_in_folder = [file for file in files_in_folder if file.endswith('.json')]
    all_rows = []
    # ok so then, given this, we have a folder with the json files, we need to process each of them
    for file in json_files_in_folder:
        # we need to process each file
        x = process_single_doc(file, path_to_root_folder)
        all_rows.append(x)

    # transform list od cits to dataframe
    df = pd.DataFrame(all_rows)
    # save dataframe to csv
    df.to_csv('final_csvs.csv')


# ok we need a main function which handles the main process pipeline
def main(folder_path: str) -> None:
    generate_pipeline_for_files_in_general_folder(folder_path)


if __name__ == '__main__':
    # args parsing
    parser = argparse.ArgumentParser(description='Process some integers.')
    # folder of the pdfs
    parser.add_argument('--pdfs-folder', type=str, default='pdfs', help='folder of the pdfs')
    # folder of the
    args = parser.parse_args()
    main(args.pdfs_folder)
