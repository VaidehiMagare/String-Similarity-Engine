"""Test cases for string similarity engine."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from similarity import (
    LevenshteinSimilarity,
    OverlapSimilarity,
    JaccardSimilarity,
    CosineSimilarity,
    SequenceSimilarity,
    HybridSimilarity
)


def run_tests():
    """Run similarity tests."""
    
    test_pairs = [
        ("hello", "hello"),
        ("hello", "helo"),
        ("hello world", "hello world"),
        ("hello world", "world hello"),
        ("The quick brown fox", "The quick brown dog"),
        ("Python programming", "Python programming language"),
        ("", ""),
        ("a", "b"),
        ("completely different", "strings here"),
    ]
    
    hybrid = HybridSimilarity()
    
    print("String Similarity Test Results")
    print("=" * 60)
    
    for str1, str2 in test_pairs:
        print(f"\nString 1: '{str1}'")
        print(f"String 2: '{str2}'")
        print("-" * 40)
        
        scores = hybrid.calculate_all(str1, str2)
        hybrid_score = hybrid.calculate_hybrid(str1, str2)
        
        for metric, score in scores.items():
            print(f"{metric:15}: {score*100:.1f}%")
        
        print(f"{'hybrid':15}: {hybrid_score*100:.1f}%")
        print("=" * 60)


if __name__ == "__main__":
    run_tests()