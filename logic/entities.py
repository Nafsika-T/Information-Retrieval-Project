import spacy
import pandas as pd
from collections import Counter, defaultdict
from multiprocessing import Pool, cpu_count
import stanza
from stanza import DownloadMethod
from queries import fetch_speeches_of_member, fetch_names_of_parties
from preprocess import preprocess_text
from visualization import visualize_entities

nlp_stanza = stanza.Pipeline('el', processors='tokenize', download_method=DownloadMethod.REUSE_RESOURCES) # Initialize Stanza pipeline for Greek language for tokenization

nlp_spacy = spacy.load('el_core_news_md') # Load the Greek language model from SpaCy for Named Entity Recognition (NER)


def extract_entities(text):
    doc_stanza = nlp_stanza(text)     

    tokens = [word.text for sent in doc_stanza.sentences for word in sent.words]   # Use Stanza to tokenize the input text

    doc_spacy = nlp_spacy(' '.join(tokens))      #Combine tokens into a single string 

    entities = [(ent.text, ent.label_) for ent in doc_spacy.ents]  # Use SpaCy to perform NER on the tokenized text

    processed_entities = []                                  # Preprocess entities and their labels
    for entity, label in entities:
        processed_entity = preprocess_text(entity)           # Clean and normalize the entities
        processed_entities.append((processed_entity, label))

    processed_entities = [(ent[0], ent[1]) for ent in processed_entities]    # Reformat processed entities into a list of tuples

    return processed_entities                               # Return processed entities with their labels


def consolidate_entities(frequency_counter):
    consolidated = defaultdict(lambda: Counter())          

    for (entity, label), freq in frequency_counter.items():  #For each entity, add the frequency of its label to the consolidated Counter
        consolidated[entity][label] += freq

    final_counter = {}
    for entity, labels in consolidated.items():                     # Keep the most frequent label for each entity
        most_common_label = labels.most_common(1)[0][0]
        total_frequency = sum(labels.values())                      # Consolidate entities with the same name but different labels, adding their frequencies together
        final_counter[(entity, most_common_label)] = total_frequency

    return final_counter                                          # Return the counter with entities and their frequencies


def extract_all_entities(member_name):
    texts = fetch_speeches_of_member(member_name, False)        # Fetch speeches of a specific member without preprocessing for better NER
    data = [speech[0] for speech in texts]

    with Pool(cpu_count()) as p:                                 # Use multiprocessing to extract entities from speeches
        all_entities = p.map(extract_entities, data)

    all_entities_flat = [item for sublist in all_entities for item in sublist]       # Flatten the list of entities from all speeches

    frequency_counter = Counter(all_entities_flat)                                  # Count the frequency of each entity-label pair

    final_counter = consolidate_entities(frequency_counter)                         # Consolidate entities with the same name but different labels

    top_entities = dict(sorted(final_counter.items(), key=lambda item: item[1], reverse=True)[:30])       # Select the top 30 most frequent entities

    df = pd.DataFrame(top_entities.items(), columns=['Entity_Label', 'Frequency'])                        # DataFrame for storing the top entities and their frequencies

    df[['Entity', 'Label']] = pd.DataFrame(df['Entity_Label'].tolist(), index=df.index)         # Split the 'Entity_Label' into separate 'Entity' and 'Label' columns

    df = df.drop(columns=['Entity_Label'])                                  # Drop the combined column

    df_sorted = df.sort_values(by='Frequency', ascending=False)             # sort by frequency

    df_sorted.to_csv("test.csv")                                            # Save the results to a CSV file

    #exit()

    visualize_entities(member_name, df_sorted)                # Visualize the top entities for the member


