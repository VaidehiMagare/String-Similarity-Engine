"""Sequence-based similarity metrics."""

from typing import Optional, List
from preprocess.text_cleaning import TextCleaner


class SequenceSimilarity:
    """Sequence matching algorithms."""
    
    def __init__(self, cleaner: Optional[TextCleaner] = None):
        self.cleaner = cleaner or TextCleaner()
    
    def longest_common_subsequence(self, str1: str, str2: str, 
                                   clean: bool = True) -> float:
        """
        Calculate similarity based on longest common subsequence.
        Returns normalized LCS length.
        """
        if clean:
            str1 = self.cleaner.clean(str1)
            str2 = self.cleaner.clean(str2)
        
        if not str1 and not str2:
            return 1.0
        if not str1 or not str2:
            return 0.0
        
        # Calculate LCS length
        m, n = len(str1), len(str2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i-1] == str2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        lcs_length = dp[m][n]
        max_length = max(len(str1), len(str2))
        
        return lcs_length / max_length if max_length > 0 else 0.0
    
    def longest_common_substring(self, str1: str, str2: str, 
                                 clean: bool = True) -> float:
        """
        Calculate similarity based on longest common substring.
        Returns normalized LCSubstring length.
        """
        if clean:
            str1 = self.cleaner.clean(str1)
            str2 = self.cleaner.clean(str2)
        
        if not str1 and not str2:
            return 1.0
        if not str1 or not str2:
            return 0.0
        
        # Calculate longest common substring length
        m, n = len(str1), len(str2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        max_length = 0
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i-1] == str2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                    max_length = max(max_length, dp[i][j])
        
        max_possible = max(len(str1), len(str2))
        
        return max_length / max_possible if max_possible > 0 else 0.0