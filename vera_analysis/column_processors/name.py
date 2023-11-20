



def get_name(document_path:str) -> str:
    name = document_path.split('.')[0]
    # add .pdf extension
    name = name + '.pdf'
    return name