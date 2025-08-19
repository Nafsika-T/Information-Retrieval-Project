import json
import pickle
from sklearn.decomposition import TruncatedSVD


def extract_topics():
    try:
        with open("Data/tfidf_matrix.pkl", "rb") as file:
            tfidf_matrix = pickle.load(file)                                 # Load the TF-IDF matrix from the file tfidf_matrix.pkl

        with open('Data/term_idf_dict.json', 'r', encoding='utf-8') as file:
            json_obj = json.load(file)                                       # Load the term IDF dictionary from the file term_idf_dict.json

        terms = json_obj.keys()                                     # Extract terms

    except IOError as ex:
        print(f"An error occurred: {ex}")
        return

    lsa = TruncatedSVD(n_components=200, random_state=42, algorithm='arpack')      # Initialize TruncatedSVD for dimensionality reduction with 200 components

    lsa.fit(tfidf_matrix)                                                          # Fit the LSA model to the TF-IDF matrix

    explained_variance_ratio = lsa.explained_variance_ratio_                       # Retrieve the explained variance ratio of each component (topic)

    with open("Data/lsa_topics.txt", "w", encoding='UTF-8') as file:                # Open the file lsa_topics.txt to write the topics and their associated terms

        for index, comp in enumerate(lsa.components_):                                  # Iterate over each component to extract topics and their terms

            terms_comp = zip(terms, comp)                                                   # iterator of tuples pairing each term with its component score

            sorted_terms = sorted(terms_comp, key=lambda x: x[1], reverse=True)[:10]        # Sort terms by their score in descending order and select the top 10 terms for each topic

            file.write("Topic " + str(index) + ":\n")                                       # Write the topic number

            for term in sorted_terms:                                                       # Write the top 10 terms for the current topic
                file.write(term[0] + '\n')

            file.write('Explained Variance of component: ' + str(explained_variance_ratio[index]) + '\n')   # Write the explained variance of the current component (topic)
            file.write('\n')

        total_explained_variance_ratio = explained_variance_ratio.sum()                             # Calculate the total explained variance ratio for all topics

        file.write(f'Total Explained Variance Ratio: {total_explained_variance_ratio:.4f}' + '\n')   # Write the total explained variance ratio for all topics
