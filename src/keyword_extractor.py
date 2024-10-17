# src/keyword_extractor.py
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from logger import logger

class KeywordExtractor:
    def extract_keywords(self, text):
        # Extract domain-specific keywords from the text using TF-IDF.
        try:
            vectorizer = TfidfVectorizer(stop_words='english', max_features=10)
            tfidf_matrix = vectorizer.fit_transform([text])
            feature_array = np.array(vectorizer.get_feature_names_out())
            tfidf_sorting = np.argsort(tfidf_matrix.toarray()).flatten()[::-1]

            top_n = 20  # Number of top keywords
            top_n_ids = tfidf_sorting[:top_n]
            keywords = feature_array[top_n_ids].tolist()
            return keywords
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []
