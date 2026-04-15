# """Hybrid similarity combining multiple metrics."""

# import numpy as np
# from typing import Optional, Dict, List
# from preprocess.text_cleaning import TextCleaner
# from config import SIMILARITY_WEIGHTS
# from .character_level import LevenshteinSimilarity
# from .overlap import OverlapSimilarity
# from .set_based import JaccardSimilarity
# from .vector_based import CosineSimilarity
# from .sequence_based import SequenceSimilarity


# class HybridSimilarity:
#     """Combines multiple similarity metrics with weighted averaging."""
    
#     def __init__(self, weights: Optional[Dict[str, float]] = None,
#                  cleaner: Optional[TextCleaner] = None):
#         self.weights = weights or SIMILARITY_WEIGHTS
#         self.cleaner = cleaner or TextCleaner()
        
#         # Initialize all similarity calculators
#         self.levenshtein = LevenshteinSimilarity(self.cleaner)
#         self.overlap = OverlapSimilarity(self.cleaner)
#         self.jaccard = JaccardSimilarity(self.cleaner)
#         self.cosine = CosineSimilarity(self.cleaner)
#         self.sequence = SequenceSimilarity(self.cleaner)
    
#     def calculate_all(self, str1: str, str2: str, 
#                      clean: bool = True) -> Dict[str, float]:
#         """Calculate all similarity scores."""
#         scores = {
#             'levenshtein': self.levenshtein.calculate(str1, str2, clean),
#             'jaccard': self.jaccard.calculate_word_jaccard(str1, str2, clean),
#             'cosine': self.cosine.calculate(str1, str2, clean),
#             'overlap': self.overlap.calculate_word_overlap(str1, str2, clean),
#             'sequence': self.sequence.longest_common_subsequence(str1, str2, clean),
#         }
        
#         # Add character-level Jaccard
#         scores['char_jaccard'] = self.jaccard.calculate_char_jaccard(str1, str2, clean)
        
#         # Add n-gram overlap
#         scores['bigram_overlap'] = self.overlap.calculate(str1, str2, clean, ngram_size=2)
        
#         return scores
    
#     def calculate_hybrid(self, str1: str, str2: str, 
#                         clean: bool = True) -> float:
#         """Calculate weighted hybrid similarity score."""
#         scores = self.calculate_all(str1, str2, clean)
        
#         weighted_sum = sum(
#             self.weights.get(metric, 0) * score
#             for metric, score in scores.items()
#             if metric in self.weights
#         )
        
#         total_weight = sum(
#             self.weights.get(metric, 0)
#             for metric in scores.keys()
#             if metric in self.weights
#         )
        
#         return weighted_sum / total_weight if total_weight > 0 else 0.0

"""Hybrid similarity combining multiple metrics including semantic."""

import numpy as np
from typing import Optional, Dict, List, Tuple
from preprocess.text_cleaning import TextCleaner
from config import SIMILARITY_WEIGHTS
from .character_level import LevenshteinSimilarity
from .overlap import OverlapSimilarity
from .set_based import JaccardSimilarity
from .vector_based import CosineSimilarity
from .sequence_based import SequenceSimilarity
from .semantic import SemanticSimilarity


class HybridSimilarity:
    """Combines multiple similarity metrics with weighted averaging."""
    
    def __init__(self, weights: Optional[Dict[str, float]] = None,
                 cleaner: Optional[TextCleaner] = None,
                 use_semantic: bool = True):
        self.weights = weights or SIMILARITY_WEIGHTS
        self.cleaner = cleaner or TextCleaner()
        self.use_semantic = use_semantic
        
        # Initialize all similarity calculators
        self.levenshtein = LevenshteinSimilarity(self.cleaner)
        self.overlap = OverlapSimilarity(self.cleaner)
        self.jaccard = JaccardSimilarity(self.cleaner)
        self.cosine = CosineSimilarity(self.cleaner)
        self.sequence = SequenceSimilarity(self.cleaner)
        
        if use_semantic:
            self.semantic = SemanticSimilarity(self.cleaner)
    
    def calculate_all(self, str1: str, str2: str, 
                     clean: bool = False) -> Dict[str, float]:
        """Calculate all similarity scores."""
        # For semantic, we don't want to clean text as it can remove meaning
        # So we pass clean=False for semantic, True for others
        
        scores = {
            'levenshtein': self.levenshtein.calculate(str1, str2, clean),
            'jaccard': self.jaccard.calculate_word_jaccard(str1, str2, clean),
            'cosine': self.cosine.calculate(str1, str2, clean),
            'overlap': self.overlap.calculate_word_overlap(str1, str2, clean),
            'sequence': self.sequence.longest_common_subsequence(str1, str2, clean),
        }
        
        if self.use_semantic:
            scores['semantic'] = self.semantic.calculate(str1, str2, clean=False)
        
        # Add additional metrics
        scores['char_jaccard'] = self.jaccard.calculate_char_jaccard(str1, str2, clean)
        scores['bigram_overlap'] = self.overlap.calculate(str1, str2, clean, ngram_size=2)
        
        return scores
    
    def calculate_hybrid(self, str1: str, str2: str, 
                        clean: bool = False) -> float:
        """Calculate weighted hybrid similarity score."""
        scores = self.calculate_all(str1, str2, clean)
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for metric, score in scores.items():
            if metric in self.weights:
                weight = self.weights[metric]
                weighted_sum += weight * score
                total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def get_similarity_breakdown(self, str1: str, str2: str) -> Dict:
        """
        Get detailed breakdown of different types of similarity.
        """
        scores = self.calculate_all(str1, str2)
        
        # Group scores by type
        lexical_scores = {
            'levenshtein': scores.get('levenshtein', 0),
            'sequence': scores.get('sequence', 0),
            'char_jaccard': scores.get('char_jaccard', 0),
        }
        
        structural_scores = {
            'jaccard': scores.get('jaccard', 0),
            'overlap': scores.get('overlap', 0),
            'bigram_overlap': scores.get('bigram_overlap', 0),
        }
        
        semantic_scores = {
            'semantic': scores.get('semantic', 0),
            'cosine': scores.get('cosine', 0),
        }
        
        # Calculate averages
        lexical_avg = np.mean(list(lexical_scores.values()))
        structural_avg = np.mean(list(structural_scores.values()))
        semantic_avg = np.mean(list(semantic_scores.values()))
        
        return {
            'all_scores': scores,
            'lexical': {
                'average': lexical_avg,
                'breakdown': lexical_scores,
                'interpretation': self._interpret_lexical(lexical_avg)
            },
            'structural': {
                'average': structural_avg,
                'breakdown': structural_scores,
                'interpretation': self._interpret_structural(structural_avg)
            },
            'semantic': {
                'average': semantic_avg,
                'breakdown': semantic_scores,
                'interpretation': self._interpret_semantic(semantic_avg)
            },
            'hybrid': self.calculate_hybrid(str1, str2)
        }
    
    def _interpret_lexical(self, score: float) -> str:
        """Interpret lexical similarity score."""
        if score >= 0.8:
            return "Very similar at character level - almost identical spelling and sequence"
        elif score >= 0.6:
            return "Moderately similar in spelling and character sequence"
        elif score >= 0.4:
            return "Some character-level similarities but noticeable differences"
        else:
            return "Significantly different in terms of spelling and character sequence"
    
    def _interpret_structural(self, score: float) -> str:
        """Interpret structural similarity score."""
        if score >= 0.7:
            return "Very similar structure and word usage patterns"
        elif score >= 0.5:
            return "Some structural similarities in word choice and arrangement"
        elif score >= 0.3:
            return "Limited structural overlap - different word choices"
        else:
            return "Very different structure and vocabulary"
    
    def _interpret_semantic(self, score: float) -> str:
        """Interpret semantic similarity score."""
        if score >= 0.85:
            return "Highly similar in meaning - essentially the same concepts expressed"
        elif score >= 0.7:
            return "Strong semantic similarity - closely related ideas"
        elif score >= 0.5:
            return "Moderate semantic connection - some shared concepts"
        elif score >= 0.3:
            return "Weak semantic relationship - slightly related topics"
        else:
            return "Semantically different - discussing different subjects"