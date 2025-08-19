# 🏛️ Greek Parliament IR System

This project implements an **Information Retrieval (IR) system** on the **Greek Parliament proceedings (September 2024)**.  
It is a web-based application that supports search, keyword extraction, named entity recognition (NER), topic modeling (LSA), and similarity detection between members.  

## 🚀 Features
- 🔍 **Search**: Returns the top-30 most relevant speeches (pagination 10/page).  
- 📝 **Keyword Extraction**: Yearly keywords for members or parties, with visualizations.  
- 🤝 **Top-K Similarities**: Finds the most similar members based on their speeches.  
- 📚 **Topic Extraction (LSA)**: 200 topics using Truncated SVD.  
- 🏷️ **Entity Recognition**: Detects persons, organizations, and locations with star-graph visualization.  

## 🛠️ Technologies
- **Backend**: Python, Flask, SQLite  
- **Frontend**: HTML, CSS, JavaScript, Bootstrap  
- **NLP/ML Libraries**: scikit-learn, SpaCy, Stanza, NLTK  
- **Visualization**: Matplotlib  

## 📂 Project Structure
- `queries.py` → SQL queries for members/parties/speeches  
- `preprocess.py` → Text preprocessing (stopwords, stemming, normalization)  
- `inverted_index.py` → Inverted index & TF-IDF retrieval  
- `keyword_extraction.py` → Yearly keyword extraction  
- `similarities.py` → Member similarity computation (cosine similarity)  
- `lsa.py` → Latent Semantic Analysis (Truncated SVD)  
- `entities.py` → Named Entity Recognition (NER)  
- `clustering.py` → Clustering (KMeans, Hierarchical)  
- `file_handler.py`, `visualization.py` → Data storage & visualizations  
- `functionality_handler.py`, `main.py`, `app.py` → Logic integration & Flask app  

## ⚙️ Installation & Run
1. Clone the repository:
   ```bash
   git clone https://github.com/username/greek-parliament-ir.git
   cd greek-parliament-ir
   ```
2. Create a virtual environment & install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app.py
   ```
4. Open in your browser:
   ```
   http://localhost:5000
   ```

## 🧩 Future Improvements
- Compress/async load large models for faster UI  
- Add IR evaluation metrics (MAP, nDCG)  
- Lightweight clustering visualization  
