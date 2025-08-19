import spacy
import unicodedata
import string
from greek_stemmer import GreekStemmer
from spacy import Language
from spacy.tokens import Doc
from queries import modify_speeches, fetch_all_speeches
from file_handler import load_stopwords

#This method applies the overall preprocessing performed on a document.
@Language.component("custom_preprocessing")
def custom_preprocessing(doc: Doc):
    cleaned_words = []

    removed_pos = ['SYM', 'ADP', 'AUX', 'ADV', 'CCONJ', 'SCONJ', 'DET', 'SPACE', 'VERB']       # List of parts-of-speech POS tags to be removed from the text

    for token in doc:                                        # Iterate over each token in the document
        word = token.text

        if token.pos_ in removed_pos or token.is_stop:       # Skip tokens with unwanted POS tags or stopwords
            continue

        cleaned_word = remove_accents(word)                  # Remove accents from the word

        cleaned_word = cleaned_word.translate(
            str.maketrans('', '', string.punctuation + "΄"))       # Remove punctuation and special characters

        stemmed_word = stemmer.stem(cleaned_word.upper())          # Apply stemming to the cleaned word

        if stemmed_word in stopwords or len(stemmed_word) <= 2:    # Skip stopwords and words that are too short
            continue

        cleaned_words.append(stemmed_word)                   # Add the processed word to the list

    return Doc(doc.vocab, cleaned_words)                # Return a new Doc object with the cleaned words


#This method preprocesses the entire set of speeches.
def preprocess_dataset():
    if stopwords is None:
        return

    speeches = fetch_all_speeches()         # Fetch all speeches from the database

    nlp.add_pipe("custom_preprocessing", after="morphologizer")

    for index, doc in enumerate(nlp.pipe(speeches, disable=["parser", "ner", "textcat", "lemmatizer"], n_process=-1)):  # Process each speech document in parallel, disabling unnecessary components
        speeches[index] = doc.text                                                                                      # Replace each speech with the processed text

    modify_speeches(speeches)      # Update the speeches in the database

#This method preprocesses a single text
def preprocess_text(text):
    for doc in nlp.pipe([text], disable=["parser", "ner", "textcat", "lemmatizer"]):
        return doc.text

#This method removes accents from the text
def remove_accents(text):
    text = ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')
    return text


stemmer = GreekStemmer()                        # Initialize the Greek stemmer

nlp = spacy.load("el_core_news_md")             # Load the SpaCy model for Greek language processing

nlp.add_pipe("custom_preprocessing", after="morphologizer")        # Add the custom preprocessing component to the pipeline

stopwords = load_stopwords()                                  # Load stopwords

# https://spacy.io/models/el
# https://spacy.io/usage/processing-pipelines#processing
