import os
import sys
import pandas


# transform ground truth xls to csv and vice versa
def transform_ground_truth(ground_truth_file_path: str, convert_to: str) -> None:
    """
    Transforms ground truth xls to csv and vice versa
    :param ground_truth_file_path: path to ground truth file
    :param convert_to: 'csv' or 'xls'
    :return: None
    """
    if convert_to == 'csv':
        df = pandas.read_excel(ground_truth_file_path)
        df.to_csv(ground_truth_file_path.replace('.xls', '.csv'), index=False)
    elif convert_to == 'xls':
        df = pandas.read_csv(ground_truth_file_path)
        df.to_excel(ground_truth_file_path.replace('.csv', '.xls'), index=False)
    else:
        raise ValueError('convert_to must be either csv or xls')


def add_data_to_csv(payload: str, document_file: str, column: str ) -> None:
    """
    Given a document, and its respective column being processed, we add the data to the csv via document_name/column location
    :param payload: data to be added
    :param document_file: document being processed
    :param column: column being processed
    :return: None
    """
