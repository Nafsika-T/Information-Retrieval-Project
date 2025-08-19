from sklearn.feature_extraction.text import TfidfVectorizer
from queries import fetch_speeches_of_member
from queries import fetch_speeches_of_party
from file_handler import write_keyword_info, read_idf_of_terms
from visualization import visualize_keywords

# This method extracts keywords from the speeches of a specific member or political party for each year

def extract_keywords_in_years(name: str, is_member=True):
    
    if is_member:                                           # Fetch speeches of a member or a party based on the input parameter
        data_from_db = fetch_speeches_of_member(name) 
    else:
        data_from_db = fetch_speeches_of_party(name)

    data_for_each_year = {}      # Dictionary to store speeches grouped by year

    for speech_details in data_from_db:                             # For each speech

        year_of_speech = speech_details[1].split('/')[2]                # Get the year of the sitting date

        if year_of_speech not in data_for_each_year.keys(): 
            data_for_each_year[year_of_speech] = [speech_details[0]]        # If the year is not already a key in the dictionary, create a new entry with the speech
        else:
            data_for_each_year[year_of_speech].append(speech_details[0])    # If the year already exists in the dictionary, append the speech to the existing list

    for year in data_for_each_year.keys():
        data_for_year = data_for_each_year[year]

        if data_for_year == [] or data_for_year is None:
            continue

        get_top_keywords(data_for_year, year, name, is_member)              # Get top keywords for the speeches of the year


# This method calculates the top n keywords for a set of speeches corresponding to a specific year
def get_top_keywords(text_data, year, name, is_member, n=15,):
    try:
        vectorizer = TfidfVectorizer(use_idf=False, lowercase=False, sublinear_tf=True)             # Initialize the TfidfVectorizer without calculating IDF

        all_speeches_combined = [' '.join(text_data)]                                               # Combine all speeches into a single string for processing

        tfidf_matrix = vectorizer.fit_transform(all_speeches_combined)                              # Compute the TF matrix for the combined speeches

        terms = vectorizer.get_feature_names_out()                                                  # Retrieve the terms used in the TF matrix

        idf = read_idf_of_terms(terms)                                                              # Read the IDF values separately for the terms (from all speeches)

        scores = [(terms[j], tfidf_matrix[0, j] * idf[j]) for j in range(tfidf_matrix.shape[1])]    # Calculate the TF-IDF score for each term by multiplying TF with the IDF

        sorted_keywords = sorted(scores, key=lambda x: x[1], reverse=True)                          # Sort terms based on their TF-IDF scores in descending order

        write_keyword_info(name, sorted_keywords[:n], year, is_member)                              # Write the top n keywords to a file

        visualize_keywords(sorted_keywords[:n], year, name, is_member)                              # Visualize the top n keywords and save the plot

    except Exception as e:
        print(e)
