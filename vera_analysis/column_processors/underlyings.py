from langchain import OpenAI, PromptTemplate
from langchain.callbacks import get_openai_callback
from dotenv import load_dotenv
import json
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from typing import List
import re

load_dotenv()


llm = OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0.5
    )


def get_underlyings(document_path:str) -> List[str]:

    with open(document_path, 'r') as f:
        loaded_json = json.loads(f.read())

    documents = loaded_json['full_text']
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0.2, separator=" ")
    texts = text_splitter.split_text(documents)
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_texts(texts, embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 4})
    underlyings_docs = retriever.get_relevant_documents("Underlying Indices", )
    prompt = PromptTemplate.from_template(
        "Take a deep breath and relax. Think step by step."
        "I have the following  document of a term sheet"
        "I need to find the Underlyings (a list of assets being invested in)"
        "Provide me with a list of the underlyings provided in the term sheet"
        "Context:"
        "{context}"
        "Given the context generate me a list of underlyings: "
    )
    full_context = ''
    for doc in underlyings_docs:
        full_context += '\n' + doc.page_content
    full_prompt = prompt.format(context=full_context)
    result = llm.invoke(full_prompt)
    # now we do a second round of checking
    import pdb; pdb.set_trace()
    final_check_template = PromptTemplate.from_template(
        "The list of underlyings is a list of stocks that the term sheet will include in its investment portfolio"
        " We have the following results from our first search for underlyings.{first_result}"
        "Take the equity stocks mentioned and put them into a python list"
    )

    final_check = final_check_template.format(first_result=result)

    final_result = llm.invoke(final_check)

    final_final_check_template = PromptTemplate.from_template(
        "The list of underlyings is a list of stocks that the term sheet will include in its investment portfolio."
        "The list of stocks has to be a list of abbreviations of the indices/stocks which are part of the underlyings." 
        "Example format: [RNO,VOW3,DAI,PAH3,GM]"
        "The first result was: {final_result}"
        "Generate a list of acronyms of the stock:"
    )

    final_final_check = final_final_check_template.format(final_result=final_result)
    final_final_result = llm.invoke(final_final_check)
    # clean final_final_result '\n\n["RNO", "VOW3", "DAI", "PAH3", "GM"]'
    res = final_final_result.replace("\n", "")


    if isinstance([final_final_result], list):
        return [res]
    else:
        final_final_check = final_final_check_template.format(final_result=final_result)
        final_final_result = llm.invoke(final_final_check)
        # clean final_final_result '\n\n["RNO", "VOW3", "DAI", "PAH3", "GM"]'
        res = final_final_result.replace("\n", "")
        return [res]
