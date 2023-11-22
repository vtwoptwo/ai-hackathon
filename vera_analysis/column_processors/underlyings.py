from langchain import PromptTemplate
from langchain.callbacks import get_openai_callback
from dotenv import load_dotenv
import json
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from typing import List, Optional
import re
from helpers.utils import instruction_response
from helpers.create_logger import create_logger
import ast
from helpers.utils import output_format_checker
load_dotenv()
import os
import time
LOG = create_logger()


def generate_full_prompt(underlyings_docs, prompt):
    full_context = ''
    for doc in underlyings_docs:
        full_context += '\n' + doc.page_content
    full_prompt = prompt.format(context=full_context)
    return full_prompt



@output_format_checker(max_attempts=10, desired_format=list)
def get_underlyings(document_path: str) -> Optional[List[str]]:
    time.sleep(10)
    # find the number of mentions of underlyings in the term sheet cap and non cap
    pattern = r'[Uu]nderlyings?'
    matches = re.findall(pattern, document_path, re.IGNORECASE)
    instances = len(matches)
    if matches == 0:
        instances = 5
    with open(document_path, 'r') as f:
        loaded_json = json.loads(f.read())
    if instances > 10:
        k = 10
    else:
        k = instances
    documents = loaded_json['full_text']
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0.2, separator=" ")
    texts = text_splitter.split_text(documents)
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_texts(texts, embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 5})
    bloomberg = retriever.get_relevant_documents("Bloomberg", )
    bbg = retriever.get_relevant_documents("BBG", )
    code = retriever.get_relevant_documents("Index Code", )

    prompt = PromptTemplate.from_template(
        "Context:"
        "{context}"
    )

    full_prompt_bloomberg = generate_full_prompt(bloomberg, prompt)
    full_prompt_bbg = generate_full_prompt(bbg, prompt)
    full_prompt_code = generate_full_prompt(code, prompt)

    result_bbg = instruction_response(full_prompt_bbg)
    result_bloomberg = instruction_response(full_prompt_bloomberg)
    result_code = instruction_response(full_prompt_code)

    list_of_results = [result_bbg, result_bloomberg, result_code]
    # now we do a second round of checking

    final_check_template = PromptTemplate.from_template(
        "The list of underlyings is a list of stocks that the term sheet will include in its investment portfolio"
        "You found the following results in the first analysis"
        "Now we need to make sure that the list of tickers is in the format of tickers"
        "{first_result}"
        "return only the list"
        "Example of your response: [ticker,ticker,...]"
    )

    final_check = final_check_template.format(first_result=list_of_results)

    final_result = instruction_response(final_check)

    pattern = r'\[[^\]]*\]'
    # Find all matches
    matches = re.findall(pattern, final_result)
    import pdb; pdb.set_trace()
    if len(matches) == 1:
        final_result = matches[0]
        final = ast.literal_eval(final_result)
        return final

    else:
        LOG.info('No matches found')

    return final_result

path = '/Users/vtwoptwo/Desktop/docs/robotics_club/hackathons/ai-hackathon/data_0611/OCR_output/XS2358486194.json'
get_underlyings(path)