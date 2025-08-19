from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from queries import fetch_speeches_of_member, fetch_names_of_members
from file_handler import read_idf_of_terms, write_most_similar_members


def find_top_simular_members(k=100):
    names_of_members = fetch_names_of_members()     # Fetch the names of all members

    speeches_grouped_by_member = []                 # List to store concatenated speeches for each member

    for name in names_of_members:                                                               #for each member:
        speeches_of_member = fetch_speeches_of_member(name)                                         # Fetch all speeches of the member

        speeches_concatenated = ' '.join([speech for speech, _ in speeches_of_member])              # Concatenate all speeches of the member into a single string

        speeches_grouped_by_member.append(speeches_concatenated)                                    # Add the concatenated speeches to the list

    vectorizer = TfidfVectorizer(sublinear_tf=True, lowercase=False, min_df=10, max_df=0.3, use_idf=False)     # Initialize the TfidfVectorizer without calculating IDF

    tf_matrix = vectorizer.fit_transform(speeches_grouped_by_member)                            # Compute the term-frequency (TF) matrix

    idf = read_idf_of_terms(vectorizer.get_feature_names_out())                                 # Read the IDF values separately for the terms (for all speeches)

    if idf is None:
        return

    tfidf_matrix = tf_matrix.toarray() * idf                                    # Multiply the TF matrix with the IDF values to produce the TF-IDF matrix

    similarity_matrix = cosine_similarity(tfidf_matrix)                         # this calculates pairwise similarities between all samples in matrix

    similarity_scores = []                                               

    num_members = len(names_of_members)

    for i in range(num_members):                                                                                      # Calculate similarity between each pair of members
        for j in range(i + 1, num_members):
            similarity_scores.append((similarity_matrix[i, j], names_of_members[i], names_of_members[j]))             # Append similarity score and member names as tuples
    similarity_scores.sort(reverse=True, key=lambda x: x[0])                                                          # Sort the similarity scores in descending order

    top_k_similar_pairs = similarity_scores[:k]                                 # Select the top k most similar member pairs

    write_most_similar_members(top_k_similar_pairs, k)       # Write the top k similar member pairs to a file

