"""Vector-based similarity metrics."""

import numpy as np
from typing import Optional, List, Dict
from collections import Counter
from preprocess.text_cleaning import TextCleaner


class CosineSimilarity:
    """Cosine similarity using TF-IDF vectors."""
    
    def __init__(self, cleaner: Optional[TextCleaner] = None):
        self.cleaner = cleaner or TextCleaner()
    
    def calculate(self, str1: str, str2: str, clean: bool = True) -> float:
        """
        Calculate cosine similarity between two strings.
        Returns value between 0 and 1.
        """
        if clean:
            str1 = self.cleaner.clean(str1)
            str2 = self.cleaner.clean(str2)
        
        # Tokenize
        tokens1 = self.cleaner.tokenize(str1, clean_first=False)
        tokens2 = self.cleaner.tokenize(str2, clean_first=False)
        
        # Create TF vectors
        tf1 = Counter(tokens1)
        tf2 = Counter(tokens2)
        
        # Get all unique terms
        all_terms = set(tf1.keys()) | set(tf2.keys())
        
        # Create vectors
        vec1 = np.array([tf1.get(term, 0) for term in all_terms])
        vec2 = np.array([tf2.get(term, 0) for term in all_terms])
        
        # Calculate cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def calculate_tfidf(self, str1: str, str2: str, clean: bool = True) -> float:
        """Calculate cosine similarity with TF-IDF weighting."""
        if clean:
            str1 = self.cleaner.clean(str1)
            str2 = self.cleaner.clean(str2)
        
        # Tokenize
        tokens1 = self.cleaner.tokenize(str1, clean_first=False)
        tokens2 = self.cleaner.tokenize(str2, clean_first=False)
        
        # Create document frequency map
        all_tokens = tokens1 + tokens2
        df = Counter(all_tokens)
        N = 2  # Number of documents
        
        # Calculate TF-IDF for first string
        tf1 = Counter(tokens1)
        tfidf1 = {}
        for term, freq in tf1.items():
            tfidf1[term] = freq * np.log(N / (1 + df[term]))
        
        # Calculate TF-IDF for second string
        tf2 = Counter(tokens2)
        tfidf2 = {}
        for term, freq in tf2.items():
            tfidf2[term] = freq * np.log(N / (1 + df[term]))
        
        # Get all terms
        all_terms = set(tfidf1.keys()) | set(tfidf2.keys())
        
        # Create vectors
        vec1 = np.array([tfidf1.get(term, 0) for term in all_terms])
        vec2 = np.array([tfidf2.get(term, 0) for term in all_terms])
        
        # Calculate cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)