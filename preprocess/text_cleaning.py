"""Text preprocessing and cleaning utilities."""

import re
import string
from typing import List, Optional
from config import PREPROCESSING_CONFIG


class TextCleaner:
    """Handles text preprocessing operations."""
    
    def __init__(self, config: Optional[dict] = None):
        self.config = config or PREPROCESSING_CONFIG
    
    def clean(self, text: str) -> str:
        """Apply all configured cleaning operations to text."""
        if not isinstance(text, str):
            text = str(text)
        
        if self.config.get('lowercase', True):
            text = text.lower()
        
        if self.config.get('remove_punctuation', True):
            text = text.translate(str.maketrans('', '', string.punctuation))
        
        if self.config.get('remove_extra_spaces', True):
            text = re.sub(r'\s+', ' ', text).strip()
        
        if self.config.get('remove_numbers', False):
            text = re.sub(r'\d+', '', text)
        
        return text
    
    def tokenize(self, text: str, clean_first: bool = True) -> List[str]:
        """Tokenize text into words."""
        if clean_first:
            text = self.clean(text)
        return text.split()
    
    def get_ngrams(self, text: str, n: int = 2, clean_first: bool = True) -> List[str]:
        """Generate n-grams from text."""
        if clean_first:
            text = self.clean(text)
        
        tokens = self.tokenize(text, clean_first=False)
        ngrams = []
        
        for i in range(len(tokens) - n + 1):
            ngram = ' '.join(tokens[i:i+n])
            ngrams.append(ngram)
        
        return ngrams
    
    def get_char_ngrams(self, text: str, n: int = 3, clean_first: bool = True) -> List[str]:
        """Generate character n-grams from text."""
        if clean_first:
            text = self.clean(text)
        
        text = text.replace(' ', '_')
        ngrams = []
        
        for i in range(len(text) - n + 1):
            ngrams.append(text[i:i+n])
        
        return ngrams