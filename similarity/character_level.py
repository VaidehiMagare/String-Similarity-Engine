"""Character-level similarity metrics."""

import Levenshtein
from typing import Optional
from preprocess.text_cleaning import TextCleaner


class LevenshteinSimilarity:
    """Levenshtein distance-based similarity."""
    
    def __init__(self, cleaner: Optional[TextCleaner] = None):
        self.cleaner = cleaner or TextCleaner()
    
    def calculate(self, str1: str, str2: str, clean: bool = True) -> float:
        """
        Calculate Levenshtein similarity ratio.
        Returns value between 0 and 1, where 1 means identical strings.
        """
        if clean:
            str1 = self.cleaner.clean(str1)
            str2 = self.cleaner.clean(str2)
        
        if not str1 and not str2:
            return 1.0
        if not str1 or not str2:
            return 0.0
        
        return Levenshtein.ratio(str1, str2)
    
    def distance(self, str1: str, str2: str, clean: bool = True) -> int:
        """Calculate raw Levenshtein distance."""
        if clean:
            str1 = self.cleaner.clean(str1)
            str2 = self.cleaner.clean(str2)
        
        return Levenshtein.distance(str1, str2)