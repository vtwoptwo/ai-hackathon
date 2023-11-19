
import json
import re
from langchain import OpenAI, PromptTemplate
from langchain.callbacks import get_openai_callback

def extract_numbers_with_context(text):
    pattern = r'(\d+(\.\d+)?)%'
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
    sentence_start = text.rfind('.', 0, start) + 1
    sentence_end = text.find('.', end)
    sentence = text[sentence_start:sentence_end].strip()
    return sentence


openai_api_key = "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"
llm = OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0.9,
        openai_api_key=openai_api_key,
        )


def llm_call(llm: OpenAI, prompt_template: str):
    with get_openai_callback() as cb:
        try:
            result = llm.invoke(prompt_template)
           
            # try:
            #     COST += float(str(cb).split(":")[-1].strip().removeprefix("$"))
            # except:
            #     LOG.info(f"DID NOT ADD COST")
            #     pass
            return result
        except Exception as e:
          print(e)

def get_cap(document_name:str) -> str:
   with open(document_name) as f:
    data = json.load(f)
    example = "{all the information}"
    text = extract_numbers_with_context(data['full_text'])
    prompt = f'''Regarding your task, you applied regex to create a dictionary where the keys are values followed by "%" in the term sheet, and each key has a list of sentences where it appears. To determine the cap, you simply need to return the numerical value associated with the term "Cap" in this dictionary. Have in mind that the value of the Underlaying cap is normally higher that 100 and that maybe that un most of the cases there is no Underlaying Cap. In that case you will just return And empty string (“”) as I showed you before. Here you have an example:
                    ##dictionary
                    {example}
                    ##answer
                    Cap: 120

                    ##dictionary
                    {example}
                    ##answer
                    Cap: 125

                    ##dictionary
                    {example}
                    ##answer
                    Cap: ""
                    
                    ## dictionary
                    {text}
                    ##answer
                    Cap:'''
    

    cap = llm_call(llm, prompt)
    return str(cap)




