from vera_analysis.main import LOG


def get_name(document_path:str) -> str:
    name = document_path.split('.')[0]
    # add .pdf extension
    name = name + '.pdf'
    LOG.info(f'Extracted name {name} from {document_path}')
    return name