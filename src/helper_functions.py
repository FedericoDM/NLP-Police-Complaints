
import spacy


def extract_entities_spacy(texts, entity_types=None, model="en_core_web_sm", batch_size=1000):
    """
    Extracts unique entities from a list of texts using SpaCy.

    Parameters:
    texts (list of str): The texts from which to extract entities.
    entity_types (list of str or str, optional): The types of entities to extract (e.g., 'PERSON', 'ORG'). 
    If None, all types are extracted.
    model (str, optional): The SpaCy model to use for entity extraction. Defaults to 'en_core_web_sm'.
    batch_size (int, optional): The number of texts to process at a time. Defaults to 1000.

    Returns:
    set: A set of unique entities extracted from the texts.
    """
    nlp = spacy.load(model)
    
    if isinstance(entity_types, str):
        entity_types = [entity_types]
    
    unique_entities = set()

    for doc in nlp.pipe(texts, batch_size=batch_size):
        for ent in doc.ents:
            if entity_types is None or ent.label_ in entity_types:
                unique_entities.add(ent.text)

    return unique_entities