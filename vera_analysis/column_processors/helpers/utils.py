import os
import sys
import pandas
import functools
from openai import OpenAI
import os


client = OpenAI()
def instruction_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a highly skilled AI trained in following instructions. You will be given an instruction and context. Answer as best as you can"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content


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


def output_format_checker(max_attempts, desired_format):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                result = func(*args, **kwargs)
                if isinstance(result, desired_format):
                    return result
                else:
                    print(f"Output '{result}' is not an instance of '{desired_format}'. Rerunning the function...")
                    attempts += 1
            raise ValueError(f"Max attempts ({max_attempts}) reached without getting the desired format '{desired_format}'")
        return wrapper
    return decorator