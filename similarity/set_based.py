"""Set-based similarity metrics."""

from typing import Optional, List, Set
from preprocess.text_cleaning import TextCleaner


class JaccardSimilarity:
    """Jaccard index for set similarity."""
    
    def __init__(self, cleaner: Optional[TextCleaner] = None):
        self.cleaner = cleaner or TextCleaner()
    
    def calculate(self, str1: str, str2: str, clean: bool = True,
                  ngram_size: int = 2) -> float:
        """
        Calculate Jaccard similarity using word n-grams.
        Returns value between 0 and 1.
        """
        if clean:
            str1 = self.cleaner.clean(str1)
            str2 = self.cleaner.clean(str2)
        
        # Get n-grams
        set1 = set(self.cleaner.get_ngrams(str1, ngram_size, clean_first=False))
        set2 = set(self.cleaner.get_ngrams(str2, ngram_size, clean_first=False))
        
        if not set1 and not set2:
            return 1.0
        if not set1 or not set2:
            return 0.0
        
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        
        return len(intersection) / len(union)
    
    def calculate_word_jaccard(self, str1: str, str2: str, clean: bool = True) -> float:
        """Calculate Jaccard similarity using individual words."""
        if clean:
            str1 = self.cleaner.clean(str1)
            str2 = self.cleaner.clean(str2)
        
        words1 = set(self.cleaner.tokenize(str1, clean_first=False))
        words2 = set(self.cleaner.tokenize(str2, clean_first=False))
        
        if not words1 and not words2:
            return 1.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def calculate_char_jaccard(self, str1: str, str2: str, 
                               clean: bool = True, n: int = 3) -> float:
        """Calculate Jaccard similarity using character n-grams."""
        if clean:
            str1 = self.cleaner.clean(str1)
            str2 = self.cleaner.clean(str2)
        
        set1 = set(self.cleaner.get_char_ngrams(str1, n, clean_first=False))
        set2 = set(self.cleaner.get_char_ngrams(str2, n, clean_first=False))
        
        if not set1 and not set2:
            return 1.0
        
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        
        return len(intersection) / len(union) if union else 0.0