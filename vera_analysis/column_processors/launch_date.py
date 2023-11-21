from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback
from dotenv import load_dotenv
import json
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import re

from final_valuation_date import re_date_pattern, open_json_and_search_key_value_pairs, get_relevant_documents, form_prompt_context_and_call_llm

load_dotenv()

llm = OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0.5
    )

synonyms = ['Launch Date', 'Trade Date']

faiss_prompt = "What is the launch date of this term sheet?"

prompt = PromptTemplate.from_template(
    "Take a deep breath and relax. Think step by step."
    "I have the following  document of a term sheet"
    "I need to find the Launch Date (which is the date that the product begins trading)"
    "The format of the launch date is usually in dd/mm/yyyy, mm/dd/yyyy, yyyy/mm/dd, or in natural language using the name of the month."
    "It is also sometimes called `Trade Date`"
    "It is really important that you get this right, because my life depends on it!\n"
    "Example:"
    "Context: Launch date 3rd July 2020"
    "Launch Date: 03/07/2020"
    "Example:"
    "Context: Launch date 2018.03.01"
    "Launch Date: 01/03/2018"

    "I am going to give you a chunk of text, and you need to tell me what is the launch date of the document\n\n"
    "You must return it in the correct date format dd/mm/yyyy and only return this value."

    "Context:{context}\n"
    "Launch Date: <your answer here>"
)


def get_launch_date(document_path:str) -> str:

    found_date, matched_synonym, full_text, json_key_value_pairs = open_json_and_search_key_value_pairs(document_path, synonyms)
    docs = get_relevant_documents(full_text, faiss_prompt)
    result = form_prompt_context_and_call_llm(docs, prompt, found_date, matched_synonym, json_key_value_pairs)
    print(result)
    matches = re.findall(re_date_pattern, result)

    if matches:
        launch_date = matches[0][0]
        return launch_date

    return None

# document_path = 'data_0611/OCR_output/XS2444480540.json'
# launch_date = get_launch_date(document_path)
# print(launch_date)
