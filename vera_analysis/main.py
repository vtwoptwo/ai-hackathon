from datetime import datetime, timedelta
import os
import json
import argparse
from typing import List
import pandas as pd
# our package functions
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
from column_processors.helpers import create_logger
from dataclasses import dataclass

LOG = create_logger()


@dataclass
class row:
    name: str  # vera v1
    isin: str  # vera v1
    issuer: str  # vera v1
    underlyings: List[str]  # vera
    currency: str  # vera v1
    strike: str  # vera
    launch_date: str  # hugo
    final_valuation_date: str  # hugo
    maturity: str  # pablo
    cap: str  # pablo
    barrier: str  # pablo



def process_single_doc(doc_name: str, folder_path:str) -> None:
    """
    Given a document, we split the processing step into several columns
    :param doc_name:
    :return:
    """
    full_path = folder_path + '/' + doc_name
    name = get_name(doc_name)
    isin = get_isin(document_path=full_path)
    issuer = get_issuer(document_path=full_path)
    underlyings = get_underlyings(document_path=full_path)
    currency = get_currency(document_path=full_path)
    strike = get_strike(full_path)
    launch_date = get_launch_date(full_path)
    final_valuation_date = get_final_valuation_date(full_path)
    maturity = get_maturity(full_path)
    cap = get_cap(document_name=full_path)
    barrier = get_barrier(document_name=full_path)

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

    # we need to get the list of files in the folder
    files_in_folder = os.listdir(path_to_root_folder)
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

    import pdb; pdb.set_trace()
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
