"""Semantic embedding models for meaning-based similarity."""

import numpy as np
from typing import List, Optional, Union
from sentence_transformers import SentenceTransformer
import torch
from config import SEMANTIC_MODEL, MAX_SEQUENCE_LENGTH, USE_MODEL_CACHE


class SemanticEmbedder:
    """Handles semantic embeddings using sentence transformers."""
    
    _instance = None
    _model = None
    
    def __new__(cls, model_name: Optional[str] = None):
        """Singleton pattern to avoid loading model multiple times."""
        if cls._instance is None:
            cls._instance = super(SemanticEmbedder, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, model_name: Optional[str] = None):
        if self._initialized:
            return
        
        self.model_name = model_name or SEMANTIC_MODEL
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self._load_model()
        self._initialized = True
    
    def _load_model(self):
        """Load the sentence transformer model."""
        try:
            if USE_MODEL_CACHE:
                self.model = SentenceTransformer(self.model_name, device=self.device)
            else:
                self.model = SentenceTransformer(self.model_name, device=self.device)
            
            # Set max sequence length
            self.model.max_seq_length = MAX_SEQUENCE_LENGTH
            
        except Exception as e:
            print(f"Error loading model {self.model_name}: {e}")
            print("Falling back to simpler model...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2', device=self.device)
    
    def encode(self, texts: Union[str, List[str]], 
               batch_size: int = 32) -> np.ndarray:
        """
        Encode texts into semantic embeddings.
        
        Args:
            texts: Single text or list of texts
            batch_size: Batch size for encoding
            
        Returns:
            Numpy array of embeddings
        """
        if isinstance(texts, str):
            texts = [texts]
        
        # Encode texts
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True  # L2 normalization for cosine similarity
        )
        
        return embeddings
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings."""
        return self.model.get_sentence_embedding_dimension()
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model."""
        return {
            'name': self.model_name,
            'device': self.device,
            'dimension': self.get_embedding_dimension(),
            'max_seq_length': self.model.max_seq_length
        }