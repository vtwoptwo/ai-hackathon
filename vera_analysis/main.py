from datetime import datetime, timedelta
import os
import json
import argparse
from typing import List

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
from helpers.create_logger import create_logger
from dataclasses import dataclass

LOG = create_logger()


@dataclass
class row:
    name: str  # vera
    isin: str  # vera
    issuer: str  # vera
    underlyings: List[str]  # vera
    currency: str  # vera
    strike: str  # hugo
    launch_date: str  # hugo
    final_valuation_date: str  # hugo
    maturity: str  # hugo
    cap: str  # pablo
    barrier: str  # pablo


def process_single_doc(doc_name: str, folder_path:str) -> None:
    """
    Given a document, we split the processing step into several columns
    :param doc_name:
    :return:
    """
    import pdb; pdb.set_trace()
    full_path = folder_path + '/' + doc_name
    name = get_name(doc_name)
    isin = get_isin(document_path=full_path)
    issuer = get_issuer(document_path=full_path)
    underlyings = get_underlyings(doc_name)
    currency = get_currency(document_path=full_path)
    strike = get_strike(doc_name)
    launch_date = get_launch_date(doc_name)
    final_valuation_date = get_final_valuation_date(doc_name)
    maturity = get_maturity(doc_name)
    cap = get_cap(doc_name)
    barrier = get_barrier(doc_name)

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

    return None


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
    # ok so then, given this, we have a folder with the json files, we need to process each of them
    for file in json_files_in_folder:
        # we need to process each file
        process_single_doc(file, path_to_root_folder)


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
