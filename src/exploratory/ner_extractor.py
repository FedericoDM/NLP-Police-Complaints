import pandas as pd
from transformers import pipeline
import os
import random

class ExtractEntities:
    def __init__(self, model="dbmdz/bert-large-cased-finetuned-conll03-english"):
        self.model = model
        self.nlp = pipeline("ner", model=model, tokenizer=model)

    def extract_entities(self, text, counts=False):
        entities = self.nlp(text)
        entity_counts = {}
        for ent in entities:
            key = (ent['word'], ent['entity'])
            entity_counts[key] = entity_counts.get(key, 0) + 1
        
        if counts:
            return [(entity, label, count) for (entity, label), count in entity_counts.items()]
        else:
            return [(entity, label) for (entity, label) in entity_counts.keys()]

    def aggregate_subwords(self, entities):
        corrected_entities = []
        previous_entity = ""
        previous_label = ""
        previous_count = 0

        for entity, label, count in entities:
            if entity.startswith("##"):
                if previous_entity:  # check if previous_entity is not empty
                    previous_entity += entity[2:]
                    previous_count += count  # agg counts for subword continuations
            else:
                if previous_entity:  # Add the previous entity if it exists
                    corrected_entities.append((previous_entity, previous_label, previous_count))
                previous_entity = entity
                previous_label = label
                previous_count = count

        # Add the last entity if the loop ends
        if previous_entity:
            corrected_entities.append((previous_entity, previous_label, previous_count))

        return corrected_entities

    def create_dataframe(self, report_number, text, counts=False):
        extracted_entities = self.extract_entities(text, counts)
        corrected_entities = self.aggregate_subwords(extracted_entities)
        df = pd.DataFrame(corrected_entities, columns=['entity', 'label', 'count'])
        df['report_number'] = report_number 
        return df

#example of usage:

# Load and preprocess the data
# cases = os.listdir(text_files_dir)
# cases = [case for case in cases if case.endswith(".txt")]
# random.seed(43)
# cases = random.sample(cases, 5)  # Randomly select 5 cases

# texts = []
# for case in cases:
#     # Extract the report number from the filename (assuming format '1234567.txt')
#     report_number = case.split('.')[0]
#     with open(os.path.join(PATH, case), 'r') as file:
#         text = file.read()
#     # Store the tuple (report_number, case_text)
#     texts.append((report_number, text))

# Call ExtractEntities, specify model bert-addresses for most usable ner model

extractor = ExtractEntities(model="ctrlbuzz/bert-addresses")

# create list of dataframes if processing more then one report
# dataframes = []
# for report_number, text in texts:
#     df = extractor.create_dataframe(report_number, text, counts=True)
#     dataframes.append(df)

# # Concatenate all dataframes to have one unified dataframe
# final_df = pd.concat(dataframes, ignore_index=True)

# Use aggregate_entities to create full entities without seperation

def aggregate_entities(df):
    aggregated_entities = []
    current_entity = ''
    current_label = ''
    report_number = ''

    for i, row in df.iterrows():
        if 'B-' in row['label']:
            if current_entity:  # Add the previous entity
                aggregated_entities.append({'entity': current_entity, 'label': current_label, 'report_number': report_number})
            current_entity = row['entity']
            current_label = row['label'].split('-')[1]  # Update the label
            report_number = row['report_number']
        elif 'I-' in row['label']:
            current_entity += f" {row['entity']}"
        else:  # Handle 'O' labels or other cases
            if current_entity:  # Add the last entity
                aggregated_entities.append({'entity': current_entity, 'label': current_label, 'report_number': report_number})
                current_entity = ''
                current_label = ''
                report_number = ''

    # Add the final entity if it exists
    if current_entity:
        aggregated_entities.append({'entity': current_entity, 'label': current_label, 'report_number': report_number})

    return pd.DataFrame(aggregated_entities)

# Example:
# aggregated_df = aggregate_entities(final_df)
# print(aggregated_df)