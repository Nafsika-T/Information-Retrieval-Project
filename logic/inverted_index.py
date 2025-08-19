import pickle
import numpy as np
from collections import defaultdict
from file_handler import read_idf_of_terms, read_lengths_of_docs
from preprocess import preprocess_text, preprocess_text
from queries import fetch_all_speeches


def default_int():
    return defaultdict(int)

#This method creates and saves the inverted index for the speeches
def write_inverted_index():

    inverted_index = defaultdict(default_int)  # Create a defaultdict to store the inverted index

    document_id = 0

    speeches = fetch_all_speeches()       # Fetch all speeches from the database

    for speech in speeches:               # For each speech
        tokens = speech.split(" ")          # Split speech into tokens

        for token in tokens:               
            inverted_index[token][document_id] += 1  # Update the inverted index with term frequencies for each document

        document_id += 1                             # Go to the next document

    try:
        with open("Data/inverted_index.pkl", "wb") as file:
            pickle.dump(inverted_index, file)                           # Save the inverted index to the file inverted_index.pkl

    except IOError as ex:
        print(f"An error occurred: {ex}")


# This method loads the inverted index from the saved file
def load_inverted_index():
    try:
        with open("Data/inverted_index.pkl", "rb") as file:
            return pickle.load(file)
    except IOError as ex:
        print(f"An error occurred: {ex}")
        return defaultdict(default_int)

# This method retrieves the top k documents for a query using the inverted index
def retrieve_top_k_docs(k, query):
    preprocessed_query = preprocess_text(query)         # Preprocess the query

    tokens = preprocessed_query.split(" ")              # Split the preprocessed query into tokens

    tokens.remove('')

    # inverted_index = load_inverted_index()

    idf = read_idf_of_terms(tokens)                     # Read the IDF values for the terms in the query from the saved file

    accumulators = defaultdict(float)                   # Accumulators for document scores

    for index, token in enumerate(tokens):                           # Calculate TF-IDF scores for each document that contains the query terms
        if token in inverted_index:
            for document_id, tf in inverted_index[token].items():
                tf_normalized = 1 + np.log(tf)                       # Calculate the normalized term frequency

                tfidf = tf_normalized * idf[index]                   # Calculate the TF-IDF score

                accumulators[document_id] += tfidf                   # Add the score to the document's accumulator

    lengths = read_lengths_of_docs(list(accumulators.keys()))        # Read the lengths of the documents for normalization

    for index, document_id in enumerate(accumulators.keys()):
        accumulators[document_id] /= lengths[index]                  # Normalize the accumulated scores by the document lengths

    sorted_docs = sorted(accumulators.items(), key=lambda item: item[1], reverse=True)     # Sort the documents by their scores in descending order

    list_of_doc = [doc_id for doc_id, score in sorted_docs[:k]]      # Get the IDs of the top k documents

    return list_of_doc                                               # Return the list of IDs of the top k documents.


inverted_index = load_inverted_index()
