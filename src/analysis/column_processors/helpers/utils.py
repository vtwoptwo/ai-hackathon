import os
import sys
import pandas
import functools
from openai import OpenAI, RateLimitError
import os
import time
from dotenv import load_dotenv

load_dotenv()
from .create_logger import create_logger

LOG = create_logger()

client = OpenAI()


def instruction_response(prompt, temp=0.5):
    response = client.chat.completions.create(
        model="gpt-4",
        temperature=temp,
        messages=[
            {
                "role": "system",
                "content": "You are a highly skilled AI trained in following instructions. You will be given an instruction and context. Answer as best as you can",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


def instruction_response_with_max_tokens(prompt, temp=0.5, max_tokens=100):
    response = client.chat.completions.create(
        model="gpt-4",
        temperature=temp,
        max_tokens=max_tokens,
        messages=[
            {
                "role": "system",
                "content": "You are a highly skilled AI trained in following instructions. You will be given an instruction and context. Answer as best as you can",
            },
            {"role": "user", "content": prompt},
        ],
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
    if convert_to == "csv":
        df = pandas.read_excel(ground_truth_file_path)
        df.to_csv(ground_truth_file_path.replace(".xls", ".csv"), index=False)
    elif convert_to == "xls":
        df = pandas.read_csv(ground_truth_file_path)
        df.to_excel(ground_truth_file_path.replace(".csv", ".xls"), index=False)
    else:
        raise ValueError("convert_to must be either csv or xls")


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
                    LOG.info(
                        f"Output '{result}' is not an instance of '{desired_format}'. Rerunning the function..."
                    )
                    attempts += 1
            return None

        return wrapper

    return decorator


def generate_full_prompt(underlyings_docs, prompt):
    full_context = ""
    for doc in underlyings_docs:
        full_context += "\n" + doc.page_content
    full_prompt = prompt.format(context=full_context)
    return full_prompt


def retry_on_rate_limit_error(max_retries=3, wait_time=30):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    result = func(*args, **kwargs)
                    return result  # If the function succeeded, return its result
                except RateLimitError as e:
                    LOG.info(
                        f"RateLimitError encountered. Retrying in {wait_time} seconds..."
                    )
                    time.sleep(wait_time)
                    retries += 1
            LOG.info(f"{RateLimitError}: Max retries reached. RateLimitError persists.")
            return None

        return wrapper

    return decorator
