"""Utility helper functions."""

from typing import Tuple
from config import SIMILARITY_THRESHOLDS


def format_score(score: float, as_percentage: bool = True) -> str:
    """Format similarity score for display."""
    if as_percentage:
        return f"{score * 100:.1f}%"
    return f"{score:.3f}"


def interpret_score(score: float) -> Tuple[str, str]:
    """
    Interpret similarity score and return category and description.
    """
    if score >= SIMILARITY_THRESHOLDS['very_high']:
        return "Very High", "Strings are nearly identical"
    elif score >= SIMILARITY_THRESHOLDS['high']:
        return "High", "Strings are very similar"
    elif score >= SIMILARITY_THRESHOLDS['medium']:
        return "Medium", "Strings have moderate similarity"
    elif score >= SIMILARITY_THRESHOLDS['low']:
        return "Low", "Strings have some similarity"
    else:
        return "Very Low", "Strings are largely different"


def get_score_color(score: float) -> str:
    """Get color for score visualization."""
    if score >= 0.9:
        return "🟢"  # Green
    elif score >= 0.7:
        return "🟡"  # Yellow
    elif score >= 0.5:
        return "🟠"  # Orange
    else:
        return "🔴"  # Red