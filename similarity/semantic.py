"""Semantic similarity using sentence transformers."""

import numpy as np
from typing import Optional, List, Dict, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from preprocess.text_cleaning import TextCleaner
from models.embeddings import SemanticEmbedder


class SemanticSimilarity:
    """Meaning-based similarity using transformer embeddings."""
    
    def __init__(self, cleaner: Optional[TextCleaner] = None,
                 model_name: Optional[str] = None):
        self.cleaner = cleaner or TextCleaner()
        self.embedder = SemanticEmbedder(model_name)
        
    def calculate(self, str1: str, str2: str, clean: bool = False) -> float:
        """
        Calculate semantic similarity between two strings.
        
        Args:
            str1: First string
            str2: Second string
            clean: Whether to clean text before encoding
            
        Returns:
            Similarity score between 0 and 1
        """
        if clean:
            str1 = self.cleaner.clean(str1)
            str2 = self.cleaner.clean(str2)
        
        if not str1.strip() or not str2.strip():
            return 0.0
        
        # Get embeddings
        embeddings = self.embedder.encode([str1, str2])
        
        # Calculate cosine similarity
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        
        # Ensure non-negative (cosine similarity can be slightly negative due to floating point)
        return max(0.0, float(similarity))
    
    def calculate_batch(self, texts: List[str], 
                        reference_text: Optional[str] = None,
                        clean: bool = False) -> List[float]:
        """
        Calculate semantic similarities for multiple texts.
        
        Args:
            texts: List of texts to compare
            reference_text: Optional reference text (if None, compare all pairs)
            clean: Whether to clean text before encoding
            
        Returns:
            List of similarity scores
        """
        if clean:
            texts = [self.cleaner.clean(t) for t in texts]
            if reference_text:
                reference_text = self.cleaner.clean(reference_text)
        
        if reference_text:
            # Compare all texts to reference
            all_texts = [reference_text] + texts
            embeddings = self.embedder.encode(all_texts)
            ref_embedding = embeddings[0]
            
            similarities = []
            for i in range(1, len(embeddings)):
                sim = cosine_similarity([ref_embedding], [embeddings[i]])[0][0]
                similarities.append(max(0.0, float(sim)))
            
            return similarities
        else:
            # Compare all pairs
            embeddings = self.embedder.encode(texts)
            n = len(texts)
            similarities = []
            
            for i in range(n):
                for j in range(i+1, n):
                    sim = cosine_similarity([embeddings[i]], [embeddings[j]])[0][0]
                    similarities.append(max(0.0, float(sim)))
            
            return similarities
    
    def get_embeddings(self, texts: List[str], 
                       clean: bool = False) -> np.ndarray:
        """Get embeddings for texts."""
        if clean:
            texts = [self.cleaner.clean(t) for t in texts]
        
        return self.embedder.encode(texts)
    
    def find_most_similar(self, query: str, candidates: List[str], 
                          top_k: int = 5, clean: bool = False) -> List[Tuple[str, float]]:
        """
        Find most similar texts to a query.
        
        Args:
            query: Query text
            candidates: List of candidate texts
            top_k: Number of top results to return
            clean: Whether to clean text
            
        Returns:
            List of (text, similarity_score) tuples
        """
        if clean:
            query = self.cleaner.clean(query)
            candidates = [self.cleaner.clean(c) for c in candidates]
        
        # Encode all texts
        all_texts = [query] + candidates
        embeddings = self.embedder.encode(all_texts)
        
        query_embedding = embeddings[0]
        candidate_embeddings = embeddings[1:]
        
        # Calculate similarities
        similarities = []
        for i, cand_emb in enumerate(candidate_embeddings):
            sim = cosine_similarity([query_embedding], [cand_emb])[0][0]
            similarities.append((candidates[i], max(0.0, float(sim))))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def analyze_semantic_relationship(self, str1: str, str2: str) -> Dict:
        """
        Analyze the semantic relationship between two strings.
        
        Returns:
            Dictionary with relationship analysis
        """
        similarity = self.calculate(str1, str2)
        
        # Determine relationship type
        if similarity >= 0.95:
            relationship = "identical"
            description = "The texts express exactly the same meaning"
        elif similarity >= 0.85:
            relationship = "paraphrase"
            description = "The texts are paraphrases of each other"
        elif similarity >= 0.75:
            relationship = "very_similar"
            description = "The texts have very similar meanings"
        elif similarity >= 0.65:
            relationship = "similar"
            description = "The texts share similar concepts and ideas"
        elif similarity >= 0.50:
            relationship = "somewhat_similar"
            description = "The texts have some semantic overlap"
        elif similarity >= 0.30:
            relationship = "slightly_related"
            description = "The texts are slightly related in meaning"
        else:
            relationship = "different"
            description = "The texts discuss different topics or concepts"
        
        return {
            'similarity': similarity,
            'relationship': relationship,
            'description': description
        }
    
    def extract_key_concepts(self, texts: List[str]) -> Dict[str, List[str]]:
        """
        Extract key concepts that are semantically similar across texts.
        
        This is a simplified version - for production, consider using
        more sophisticated NLP techniques like topic modeling.
        """
        # This is a placeholder for more advanced semantic analysis
        # In practice, you might use BERT-based keyword extraction or topic modeling
        
        return {
            'common_themes': ['theme1', 'theme2'],  # Placeholder
            'semantic_clusters': []
        }