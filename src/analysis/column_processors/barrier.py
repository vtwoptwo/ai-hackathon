import json
import re
from .helpers.utils import instruction_response, retry_on_rate_limit_error


def extract_numbers_with_context(text):
    pattern = r"(\d+(\.\d+)?)%"
    matches = re.finditer(pattern, text)

    result_dict = {}

    for match in matches:
        number = float(match.group(1))
        sentence = find_sentence_containing_number(text, match.start(), match.end())

        # Update the result_dict with the number and its corresponding sentence
        if number in result_dict:
            result_dict[number].append(sentence)
        else:
            result_dict[number] = [sentence]

    return result_dict


def find_sentence_containing_number(text, start, end):
    # Find the sentence containing the matched number
    sentence_start = text.rfind(".", 0, start) + 1
    sentence_end = text.find(".", end)
    sentence = text[sentence_start:sentence_end].strip()
    return sentence


@retry_on_rate_limit_error(wait_time=30)
def get_barrier(document_name: str) -> str:
    with open(document_name) as f:
        data = json.load(f)
        # print(data["key-value_pairs"].keys())
        example = "{all the information}"
        text = extract_numbers_with_context(data["full_text"])
        for key in list(text.keys()):
            if int(key) < 55 or int(key) > 99:
                del text[key]
        # print(text)
        prompt = f"""In a term sheet, a "barrier" also known as KNOCK-OUT is a pre-established condition, often indicated as a percentage, that must be achieved for specific terms to become active. For instance, if there is a 65% barrier, it means that a particular provision or benefit takes effect only when a related metric or target reaches 65% of its designated objective.
                Regarding your task, you applied regex to create a dictionary where the keys are values followed by "%" in the term sheet, and each key has a list of sentences where it appears. Read carefully each sentence. 
                To determine the barrier, you simply need to return the numerical value associated with the term "barrier" in this dictionary. You MUST return a value among {text.keys()}. The result cannot be None.  Take a deep breath and relax. Think step by step
                 Here you have an example:
                ##dictionary
                {example}
                ##answer
                Barrier: 70
                ##dictionary
                {example}
                ##answer
                Barrier: 60
                ## dictionary
                {example}
                Barrier: 65

                ## dictionary
                {text}
                Barrier:"""

        barrier = instruction_response(prompt).strip()
        barrier2 = instruction_response(prompt).strip()
        barrier3 = instruction_response(prompt).strip()
        barrier4 = instruction_response(prompt).strip()

        barrier_list = [barrier, barrier2, barrier3, barrier4]
        # print(barrier_list)
        barrier = max(barrier_list, key=barrier_list.count)

        confirmation_prompt = f"""Given the following information, please just output the barrier value.
        ##sentence
        'The barrier is 60.º
        ##answer
        60
        ##sentence
        'Barrier: 65'
        ##answer
        65
        ##sentence
        {barrier}
        ##answer"""
        barrier = instruction_response(confirmation_prompt).strip()
        # print(barrier)
        return str(barrier)
