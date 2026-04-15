"""Main entry point for string similarity engine."""

from similarity import HybridSimilarity
from preprocess import TextCleaner
from utils import format_score, interpret_score


def compare_strings(str1: str, str2: str, verbose: bool = False):
    """Compare two strings and return similarity scores."""
    
    # Initialize
    hybrid = HybridSimilarity()
    
    # Calculate scores
    scores = hybrid.calculate_all(str1, str2)
    hybrid_score = hybrid.calculate_hybrid(str1, str2)
    
    if verbose:
        print(f"\nComparing:")
        print(f"String 1: '{str1}'")
        print(f"String 2: '{str2}'")
        print("\n" + "="*50)
        print("Similarity Scores:")
        print("-"*50)
        
        for metric, score in scores.items():
            category, _ = interpret_score(score)
            formatted = format_score(score)
            print(f"{metric:20}: {formatted:8} ({category})")
        
        print("-"*50)
        hybrid_formatted = format_score(hybrid_score)
        hybrid_category, _ = interpret_score(hybrid_score)
        print(f"{'Hybrid Score':20}: {hybrid_formatted:8} ({hybrid_category})")
        print("="*50)
    
    return {
        'scores': scores,
        'hybrid_score': hybrid_score,
        'interpretation': interpret_score(hybrid_score)
    }


if __name__ == "__main__":
    # Example usage
    str1 = "The quick brown fox jumps over the lazy dog"
    str2 = "The quick brown cat jumps over the lazy dog"
    
    result = compare_strings(str1, str2, verbose=True)