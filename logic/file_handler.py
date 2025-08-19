import json
import os
import pickle
import linecache
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from queries import fetch_all_speeches


# This method creates an appropriate folder (depending on whether the name refers to a member or a party) 
# and writes the keywords related to a specific year into a file named keywords.txt.
def write_keyword_info(name, keywords, year, is_member):
    if keywords == [] or keywords is None:
        return

    if is_member:
        directory = f'Data/parliament_data/parliament_member/{name}'
    else:
        directory = f'Data/parliament_data/parliament_party/{name}'

    os.makedirs(directory, exist_ok=True)

    year_directory = os.path.join(directory, year)

    os.makedirs(year_directory, exist_ok=True)

    file_path = os.path.join(year_directory, 'keywords.txt')

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"Year: {year}" + '\n')

        for keyword in keywords:
            file.write(keyword[0] + ': ' + str(keyword[1]) + '\n')

# This method calculates the TF-IDF values for all speeches and the length of each document 
# and saves them in the corresponding files (term_idf_dict.json, tfidf_matrix.pkl, document_lengths.txt).
def write_tfidf_files():
    speeches = fetch_all_speeches()

    tfidf_vectorizer = TfidfVectorizer(min_df=10, max_df=0.3, lowercase=False, sublinear_tf=True, norm=None)

    tfidf_matrix = tfidf_vectorizer.fit_transform(speeches)

    vocabulary = tfidf_vectorizer.vocabulary_

    idf = tfidf_vectorizer.idf_

    for key in dict(vocabulary).keys():
        vocabulary[key] = idf[vocabulary[key]]

    try:
        with open("Data/document_lengths.txt", 'w', encoding='utf-8') as file:
            for doc_id in range(len(speeches)):
                doc_vector = tfidf_matrix[doc_id]

                length = np.sqrt(sum((weight ** 2 for weight in doc_vector.data)))
                file.write(str(length) + '\n')

        with open('Data/term_idf_dict.json', 'w', encoding='utf-8') as file:
            json.dump(vocabulary, file, ensure_ascii=False, indent=4)

        with open('Data/tfidf_matrix.pkl', 'wb') as file:
            pickle.dump(tfidf_matrix, file)
    except IOError as ex:
        print(f"An error occurred: {ex}")

# This method reads the lengths of specific documents from the file document_lengths.txt
def read_lengths_of_docs(ids):
    lengths = []
    for doc_id in ids:
        length = linecache.getline('Data/document_lengths.txt', doc_id)

        lengths.append(float(length))
    return lengths

# This method reads the IDF weights for specific terms from the file term_idf_dict.json
# If a term is not present in the vocabulary, it returns 0 for that term
def read_idf_of_terms(terms):
    try:
        with open('Data/term_idf_dict.json', 'r', encoding='utf-8') as file:
            json_obj = json.load(file)

        result = [json_obj.get(term) if json_obj.get(term) is not None else 0 for term in terms]

        return result

    except IOError as ex:
        print(f"An error occurred: {ex}")

        return None

# This method writes the k most similar members of parliament to a file named most_similar_members.txt
# The data is provided as triplets, where each triplet includes the similarity score and the names of the two members
def write_most_similar_members(triplets, k):
    try:
        with open(f'Data/{k}_most_similar_members.txt', 'w', encoding='utf-8') as file:
            for triplet in triplets:
                file.write(triplet[1] + ', ' + triplet[2] + ': ' + str(triplet[0]) + '\n')

    except IOError as ex:

        print(f"An error occurred: {ex}")

# This method loads a list of stopwords from the file stopwords-el.txt and returns them
def load_stopwords():
    try:
        with open('Data/stopwords-el.txt', 'r', encoding='utf-8') as file:
            stopwords_from_file = file.read().splitlines()

        return stopwords_from_file
    except IOError as ex:
        print(f"An error occurred: {ex}")

        return None
