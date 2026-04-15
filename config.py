# """Configuration settings for the string similarity engine."""

# # Preprocessing settings
# PREPROCESSING_CONFIG = {
#     'lowercase': True,
#     'remove_punctuation': True,
#     'remove_extra_spaces': True,
#     'remove_numbers': False,
#     'remove_stopwords': False,
# }

# # Similarity weights for hybrid score
# SIMILARITY_WEIGHTS = {
#     'levenshtein': 0.25,
#     'jaccard': 0.20,
#     'cosine': 0.25,
#     'overlap': 0.15,
#     'sequence': 0.15,
# }

# # Thresholds for interpretation
# SIMILARITY_THRESHOLDS = {
#     'very_high': 0.9,
#     'high': 0.7,
#     'medium': 0.5,
#     'low': 0.3,
#     'very_low': 0.0,
# }

# # N-gram settings
# NGRAM_RANGE = (2, 4)

"""Configuration settings for the string similarity engine."""

# Preprocessing settings
PREPROCESSING_CONFIG = {
    'lowercase': True,
    'remove_punctuation': True,
    'remove_extra_spaces': True,
    'remove_numbers': False,
    'remove_stopwords': False,
}

# Similarity weights for hybrid score (Updated with semantic)
SIMILARITY_WEIGHTS = {
    'levenshtein': 0.15,
    'jaccard': 0.10,
    'cosine': 0.15,
    'overlap': 0.10,
    'sequence': 0.10,
    'semantic': 0.40,  # Higher weight for meaning-based similarity
}

# Thresholds for interpretation
SIMILARITY_THRESHOLDS = {
    'very_high': 0.9,
    'high': 0.7,
    'medium': 0.5,
    'low': 0.3,
    'very_low': 0.0,
}

# N-gram settings
NGRAM_RANGE = (2, 4)

# Semantic model settings
SEMANTIC_MODEL = 'all-MiniLM-L6-v2'  # Fast and efficient model
# Alternative models:
# 'all-mpnet-base-v2' - Better quality but slower
# 'paraphrase-MiniLM-L6-v2' - Good for paraphrase detection
# 'distiluse-base-multilingual-cased-v2' - Multilingual support

# Cache settings
USE_MODEL_CACHE = True
MAX_SEQUENCE_LENGTH = 256