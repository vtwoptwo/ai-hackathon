from datetime import datetime, timedelta
import os
import json
import argparse
from typing import List
import pandas as pd
from column_processors.isin import get_isin
from column_processors.issuer import get_issuer
from column_processors.name import get_name
from column_processors.underlyings import get_underlyings, retry_underlyings
from column_processors.currency import get_currency
from column_processors.strike import get_strike
from column_processors.launch_date import get_launch_date
from column_processors.final_valuation_date import get_final_valuation_date
from column_processors.maturity import get_maturity
from column_processors.cap import get_cap
from column_processors.barrier import get_barrier
from column_processors.helpers.create_logger import create_logger
from column_processors.helpers.utils import retry_on_rate_limit_error
from column_processors.maturity_and_final import get_maturity_and_final_date
from dataclasses import dataclass
from ocr import perform_ocr

# randomize the json_files_in_folder using shuffle
import random
import sys

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


def process_single_doc(doc_name: str, folder_path: str) -> row:
    """
    Given a document, we split the processing step into several columns
    :param doc_name:
    :return:
    """

    full_path = folder_path + "/" + doc_name
    LOG.info(f"Starting Pipeline for {doc_name}")

    # underlyings
    LOG.info("Processing underlyings")
    underlyings = get_underlyings(document_path=full_path)
    LOG.info(f"Processed underlyings: {underlyings}")

    # strike
    LOG.info("Processing strike")
    strike = get_strike(full_path)
    LOG.info(f"Processed strike: {strike}")

    max = 5
    count = 0

    if strike is None:
        strike = []
    if underlyings is None:
        underlyings = []

    if len(underlyings) != len(strike):
        while len(underlyings) != len(strike) and count <= max:
            LOG.info("Retrying underlyings and strike: {count}")
            underlyings, strike = retry_underlyings(
                document_path=full_path,
                prev_underlyings=underlyings,
                prev_strike=strike,
            )
            count += 1

    LOG.info("Processing Maturity and final valuation date")
    dates = get_maturity_and_final_date(full_path)
    LOG.info(f"Processed valuation date: {dates}")

    if dates is None:
        final_valuation_date = []
        maturity = []
    else:
        final_valuation_date = dates[0]
        maturity = dates[1]

    # name
    LOG.info("Processing Name")
    name = get_name(doc_name)
    LOG.info(f"Processed name {name}")

    # isin
    LOG.info("Processing isin")
    isin = get_isin(document_path=full_path)
    LOG.info(f"Processed isin: {isin}")

    # issuer
    LOG.info("Processing issuer")
    issuer = get_issuer(document_path=full_path)
    LOG.info(f"Processed issuer:{issuer}")

    LOG.info("Processing currency")
    currency = get_currency(document_path=full_path)
    LOG.info(f"Processed currency: {currency}")

    LOG.info("Processing launch date")
    launch_date = get_launch_date(full_path)
    LOG.info(f"Processed launch_date: {launch_date}")

    # LOG.info("Processing final valuation date")
    # final_valuation_date = get_final_valuation_date(full_path)
    # LOG.info(f"Processed final_valuation date: {final_valuation_date}")
    #

    LOG.info("Processing cap")
    cap = get_cap(document_name=full_path)
    LOG.info(f"Processed cap: {cap}")

    LOG.info("Processing barrier")
    barrier = get_barrier(document_name=full_path)
    LOG.info(f"Processed barrier: barrier")

    if count > max:
        LOG.info("Max retries reached, using the previous values")
        final_output = row(
            name=name,
            isin=isin,
            issuer=issuer,
            underlyings=underlyings,
            currency=currency,
            strike=strike,
            launch_date=launch_date,
            final_valuation_date=final_valuation_date,
            maturity=maturity,
            cap=cap,
            barrier=barrier,
        )
    else:
        final_output = row(
            name=name,
            isin=isin,
            issuer=issuer,
            underlyings=underlyings,
            currency=currency,
            strike=strike,
            launch_date=launch_date,
            final_valuation_date=final_valuation_date,
            maturity=maturity,
            cap=cap,
            barrier=barrier,
        )

    LOG.info(f"Processed {doc_name} with row {final_output}")

    row_final = {
        "name": final_output.name,
        "isin": final_output.isin,
        "issuer": final_output.issuer,
        "underlyings": final_output.underlyings,
        "currency": final_output.currency,
        "strike": final_output.strike,
        "launch_date": final_output.launch_date,
        "final_valuation_date": final_output.final_valuation_date,
        "maturity": final_output.maturity,
        "cap": final_output.cap,
        "barrier": final_output.barrier,
    }

    return row_final


def generate_pipeline_for_files_in_general_folder(
    path_to_root_folder: str, destination: str, ocr_destination: str
) -> None:
    path_to_root_folder = os.path.abspath(path_to_root_folder)
    LOG.info(f"Processing files in {path_to_root_folder}")

    output_ocr = ocr_destination
    # get current path
    # we need to get the list of files in the folder
    if output_ocr not in os.listdir(path_to_root_folder):
        os.mkdir(path_to_root_folder + "/" + output_ocr)

    LOG.info(f"Performing OCR on {path_to_root_folder}")

    perform_ocr(path_to_root_folder, output_ocr)

    files_in_folder = os.listdir(path_to_root_folder + "/" + output_ocr)

    json_files_in_folder = [file for file in files_in_folder if file.endswith(".json")]
    all_rows = []

    # ok so then, given this, we have a folder with the json files, we need to process each of them
    for file in json_files_in_folder:
        # we need to process each file
        x = process_single_doc(file, path_to_root_folder + output_ocr)
        all_rows.append(x)

    # transform list od cits to dataframe
    df = pd.DataFrame(all_rows)
    # save dataframe to csv
    df.to_csv(destination)

    return None


# ok we need a main function which handles the main process pipeline
def main(folder_path: str, destination: str, ocr_destination: str) -> None:
    generate_pipeline_for_files_in_general_folder(
        folder_path, destination, ocr_destination
    )


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument(
        "-origin_file", default="../../src/test_data", help="file to be processed"
    )
    parse.add_argument(
        "-destination_file", default="./predictions.csv", help="file to be saved"
    )
    parse.add_argument(
        "-ocr_destination", default="OCR_OUTPUT", help="ocr Destination files"
    )
    args = parse.parse_args()

    origin_file = args.origin_file
    destination_file = args.destination_file
    ocr_destination = args.ocr_destination

    main(origin_file, destination_file, ocr_destination)
