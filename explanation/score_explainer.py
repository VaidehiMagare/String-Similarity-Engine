# """Generate explanations for similarity scores."""

# from typing import Dict, List, Tuple
# import numpy as np


# class ScoreExplainer:
#     """Generates human-readable explanations for similarity scores."""
    
#     def __init__(self):
#         self.metric_descriptions = {
#             'levenshtein': {
#                 'name': 'Levenshtein Ratio',
#                 'description': 'Measures character-level edits needed to transform one string into another',
#                 'interpretation': {
#                     'high': 'Strings require very few character changes to match',
#                     'medium': 'Strings require moderate character changes to match',
#                     'low': 'Strings require many character changes to match'
#                 }
#             },
#             'jaccard': {
#                 'name': 'Jaccard Index',
#                 'description': 'Measures overlap of word sets between strings',
#                 'interpretation': {
#                     'high': 'Strings share many of the same words',
#                     'medium': 'Strings share some common words',
#                     'low': 'Strings share very few words'
#                 }
#             },
#             'cosine': {
#                 'name': 'Cosine Similarity',
#                 'description': 'Measures similarity of word frequency patterns',
#                 'interpretation': {
#                     'high': 'Word usage patterns are very similar',
#                     'medium': 'Word usage patterns have some similarity',
#                     'low': 'Word usage patterns are different'
#                 }
#             },
#             'overlap': {
#                 'name': 'Overlap Coefficient',
#                 'description': 'Measures how much of the smaller string\'s content appears in the larger',
#                 'interpretation': {
#                     'high': 'Most words from the shorter string appear in the longer one',
#                     'medium': 'Some words from the shorter string appear in the longer one',
#                     'low': 'Few words from the shorter string appear in the longer one'
#                 }
#             },
#             'sequence': {
#                 'name': 'Sequence Similarity',
#                 'description': 'Measures longest common sequence of characters',
#                 'interpretation': {
#                     'high': 'Strings share long common sequences',
#                     'medium': 'Strings share some common sequences',
#                     'low': 'Strings share few common sequences'
#                 }
#             }
#         }
    
#     def generate_explanation(self, scores: Dict[str, float], 
#                             str1: str, str2: str) -> str:
#         """Generate comprehensive explanation of similarity scores."""
        
#         # Calculate average score for overall assessment
#         avg_score = np.mean(list(scores.values()))
        
#         # Start building explanation
#         explanation = []
        
#         # Overall assessment
#         explanation.append("## 📊 Overall Similarity Assessment\n")
#         explanation.append(self._get_overall_assessment(avg_score))
#         explanation.append("\n")
        
#         # Detailed metric explanations
#         explanation.append("## 🔍 Detailed Analysis\n")
        
#         # Sort metrics by score (highest first)
#         sorted_metrics = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
#         for metric, score in sorted_metrics:
#             if metric in self.metric_descriptions:
#                 explanation.append(self._format_metric_explanation(
#                     metric, score, str1, str2
#                 ))
        
#         # Specific observations
#         explanation.append("## 💡 Key Observations\n")
#         explanation.extend(self._get_specific_observations(scores, str1, str2))
        
#         return "\n".join(explanation)
    
#     def _get_overall_assessment(self, avg_score: float) -> str:
#         """Generate overall assessment based on average score."""
#         if avg_score >= 0.9:
#             return "These strings are **extremely similar** - they are nearly identical in both content and structure."
#         elif avg_score >= 0.7:
#             return "These strings are **highly similar** - they share significant content and structure."
#         elif avg_score >= 0.5:
#             return "These strings have **moderate similarity** - they share some common elements but also have notable differences."
#         elif avg_score >= 0.3:
#             return "These strings have **low similarity** - they share only a few common elements."
#         else:
#             return "These strings are **very different** - they share minimal common elements."
    
#     def _format_metric_explanation(self, metric: str, score: float,
#                                    str1: str, str2: str) -> str:
#         """Format explanation for a specific metric."""
#         info = self.metric_descriptions[metric]
        
#         # Determine interpretation level
#         if score >= 0.7:
#             level = 'high'
#             emoji = '🟢'
#         elif score >= 0.5:
#             level = 'medium'
#             emoji = '🟡'
#         else:
#             level = 'low'
#             emoji = '🔴'
        
#         explanation = f"### {emoji} {info['name']}: {score*100:.1f}%\n"
#         explanation += f"*{info['description']}*\n\n"
#         explanation += f"**What this means:** {info['interpretation'][level]}\n\n"
        
#         # Add specific example if relevant
#         if metric == 'levenshtein' and score > 0.5:
#             explanation += self._get_levenshtein_example(str1, str2)
#         elif metric == 'jaccard' and score > 0.3:
#             explanation += self._get_jaccard_example(str1, str2)
        
#         return explanation
    
#     def _get_levenshtein_example(self, str1: str, str2: str) -> str:
#         """Generate Levenshtein-specific example."""
#         common_prefix = self._find_common_prefix(str1, str2)
#         if len(common_prefix) > 3:
#             return f"**Example:** Both strings start with \"{common_prefix}\"\n\n"
#         return ""
    
#     def _get_jaccard_example(self, str1: str, str2: str) -> str:
#         """Generate Jaccard-specific example."""
#         words1 = set(str1.lower().split())
#         words2 = set(str2.lower().split())
#         common = words1.intersection(words2)
        
#         if common:
#             common_list = list(common)[:3]
#             return f'**Example:** Common words include: {", ".join([f"{w}" for w in common_list])}\n\n'
#         return ""
    
#     def _find_common_prefix(self, str1: str, str2: str) -> str:
#         """Find common prefix of two strings."""
#         min_len = min(len(str1), len(str2))
#         for i in range(min_len):
#             if str1[i] != str2[i]:
#                 return str1[:i]
#         return str1[:min_len]
    
#     def _get_specific_observations(self, scores: Dict[str, float],
#                                    str1: str, str2: str) -> List[str]:
#         """Generate specific observations about the strings."""
#         observations = []
        
#         # Length comparison
#         len_diff = abs(len(str1) - len(str2))
#         if len_diff == 0:
#             observations.append("- Both strings have **exactly the same length**.")
#         elif len_diff <= 5:
#             observations.append(f"- String lengths differ by only **{len_diff} characters**.")
#         else:
#             observations.append(f"- String lengths differ by **{len_diff} characters**.")
        
#         # Word count comparison
#         words1 = len(str1.split())
#         words2 = len(str2.split())
#         if words1 == words2:
#             observations.append("- Both strings have the **same number of words**.")
        
#         # Check for substring relationship
#         if str1 in str2:
#             observations.append("- The **first string is completely contained** within the second string.")
#         elif str2 in str1:
#             observations.append("- The **second string is completely contained** within the first string.")
        
#         # Check for high scores
#         if scores.get('levenshtein', 0) > 0.9:
#             observations.append("- **Character-level match is very high** - strings are nearly identical letter-by-letter.")
        
#         if scores.get('jaccard', 0) > 0.8:
#             observations.append("- **Word usage is very similar** - strings share most of their vocabulary.")
        
#         return observations

"""Generate explanations for similarity scores including semantic analysis."""

from typing import Dict, List, Tuple
import numpy as np


class ScoreExplainer:
    """Generates human-readable explanations for similarity scores."""
    
    def __init__(self):
        self.metric_descriptions = {
            'levenshtein': {
                'name': 'Levenshtein Ratio',
                'description': 'Measures character-level edits needed to transform one string into another',
                'interpretation': {
                    'high': 'Strings require very few character changes to match',
                    'medium': 'Strings require moderate character changes to match',
                    'low': 'Strings require many character changes to match'
                }
            },
            'jaccard': {
                'name': 'Jaccard Index',
                'description': 'Measures overlap of word sets between strings',
                'interpretation': {
                    'high': 'Strings share many of the same words',
                    'medium': 'Strings share some common words',
                    'low': 'Strings share very few words'
                }
            },
            'cosine': {
                'name': 'Cosine Similarity',
                'description': 'Measures similarity of word frequency patterns',
                'interpretation': {
                    'high': 'Word usage patterns are very similar',
                    'medium': 'Word usage patterns have some similarity',
                    'low': 'Word usage patterns are different'
                }
            },
            'semantic': {
                'name': 'Semantic Similarity',
                'description': 'Measures meaning-based similarity using AI embeddings',
                'interpretation': {
                    'high': 'Texts express very similar meanings and concepts',
                    'medium': 'Texts share some conceptual similarity',
                    'low': 'Texts discuss different topics or ideas'
                }
            },
            'overlap': {
                'name': 'Overlap Coefficient',
                'description': 'Measures how much of the smaller string\'s content appears in the larger',
                'interpretation': {
                    'high': 'Most words from the shorter string appear in the longer one',
                    'medium': 'Some words from the shorter string appear in the longer one',
                    'low': 'Few words from the shorter string appear in the longer one'
                }
            },
            'sequence': {
                'name': 'Sequence Similarity',
                'description': 'Measures longest common sequence of characters',
                'interpretation': {
                    'high': 'Strings share long common sequences',
                    'medium': 'Strings share some common sequences',
                    'low': 'Strings share few common sequences'
                }
            }
        }
    
    def generate_explanation(self, scores: Dict[str, float], 
                            str1: str, str2: str,
                            breakdown: Dict = None) -> str:
        """Generate comprehensive explanation including semantic analysis."""
        
        # Calculate average score for overall assessment
        avg_score = np.mean(list(scores.values()))
        
        # Start building explanation
        explanation = []
        
        # Overall assessment
        explanation.append("## 📊 Overall Similarity Assessment\n")
        explanation.append(self._get_overall_assessment(avg_score))
        
        # Semantic-specific assessment
        if 'semantic' in scores:
            explanation.append("\n### 🧠 Semantic Analysis\n")
            explanation.append(self._get_semantic_assessment(scores['semantic'], str1, str2))
        
        explanation.append("\n")
        
        # Detailed breakdown by category
        if breakdown:
            explanation.append("## 📈 Similarity Breakdown by Category\n")
            explanation.append(self._format_category_breakdown(breakdown))
            explanation.append("\n")
        
        # Detailed metric explanations
        explanation.append("## 🔍 Detailed Metric Analysis\n")
        
        # Sort metrics by score (highest first)
        sorted_metrics = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        for metric, score in sorted_metrics:
            if metric in self.metric_descriptions:
                explanation.append(self._format_metric_explanation(
                    metric, score, str1, str2
                ))
        
        # Specific observations
        explanation.append("## 💡 Key Observations\n")
        explanation.extend(self._get_specific_observations(scores, str1, str2))
        
        # Add semantic insights
        if 'semantic' in scores:
            explanation.append("\n### 🔮 Semantic Insights\n")
            explanation.extend(self._get_semantic_insights(scores['semantic'], str1, str2))
        
        return "\n".join(explanation)
    
    def _get_semantic_assessment(self, score: float, str1: str, str2: str) -> str:
        """Generate semantic-specific assessment."""
        if score >= 0.9:
            return "✅ **Meaning Match: Excellent**\n\nThe texts express virtually identical meanings. Even if the wording is different, the underlying concepts and ideas are the same."
        elif score >= 0.8:
            return "🟢 **Meaning Match: Very Good**\n\nThe texts are semantically very close - they discuss the same topics with very similar meaning."
        elif score >= 0.7:
            return "🟡 **Meaning Match: Good**\n\nStrong semantic similarity detected. The texts share major concepts and themes."
        elif score >= 0.6:
            return "🟠 **Meaning Match: Moderate**\n\nThere is noticeable semantic overlap, though the texts may emphasize different aspects."
        elif score >= 0.5:
            return "🟤 **Meaning Match: Fair**\n\nSome semantic connection exists, but the texts diverge in meaning significantly."
        elif score >= 0.3:
            return "🔴 **Meaning Match: Weak**\n\nLimited semantic relationship - the texts discuss loosely related topics."
        else:
            return "⚫ **Meaning Match: Very Weak**\n\nThe texts are semantically unrelated - they discuss different subjects entirely."
    
    def _format_category_breakdown(self, breakdown: Dict) -> str:
        """Format the categorical breakdown of similarities."""
        text = []
        
        if 'lexical' in breakdown:
            lex = breakdown['lexical']
            text.append(f"**Character-Level Similarity:** {lex['average']*100:.1f}%")
            text.append(f"_{lex['interpretation']}_\n")
        
        if 'structural' in breakdown:
            struct = breakdown['structural']
            text.append(f"**Structural Similarity:** {struct['average']*100:.1f}%")
            text.append(f"_{struct['interpretation']}_\n")
        
        if 'semantic' in breakdown:
            sem = breakdown['semantic']
            text.append(f"**Meaning-Based Similarity:** {sem['average']*100:.1f}%")
            text.append(f"_{sem['interpretation']}_\n")
        
        return "\n".join(text)
    
    def _get_semantic_insights(self, score: float, str1: str, str2: str) -> List[str]:
        """Generate semantic insights."""
        insights = []
        
        # Length comparison for context
        len1, len2 = len(str1.split()), len(str2.split())
        
        if score > 0.7:
            if len1 != len2:
                insights.append(f"- Despite different lengths ({len1} vs {len2} words), the **meaning is well preserved**.")
            else:
                insights.append("- The texts are **semantically aligned** with consistent meaning.")
            
            insights.append("- These texts could be considered **paraphrases** of each other.")
        
        elif score > 0.5:
            insights.append("- The texts share **common themes** but express them differently.")
            
            # Check for potential keyword overlap
            words1 = set(str1.lower().split())
            words2 = set(str2.lower().split())
            common = words1.intersection(words2)
            
            if common:
                sample = list(common)[:3]
                insights.append(f"- Common keywords like {', '.join(f'**{w}**' for w in sample)} indicate shared topics.")
        
        else:
            insights.append("- The texts appear to discuss **different subjects or perspectives**.")
            
            # Check if there's any common ground
            words1 = set(str1.lower().split())
            words2 = set(str2.lower().split())
            common = words1.intersection(words2)
            
            if common:
                insights.append(f"- However, they share some vocabulary ({len(common)} common words), suggesting **tangential relatedness**.")
        
        return insights
    
    def _get_overall_assessment(self, avg_score: float) -> str:
        """Generate overall assessment based on average score."""
        if avg_score >= 0.9:
            return "These strings are **extremely similar** - they are nearly identical in both content, structure, and meaning."
        elif avg_score >= 0.7:
            return "These strings are **highly similar** - they share significant content, structure, and meaning."
        elif avg_score >= 0.5:
            return "These strings have **moderate similarity** - they share some common elements but also have notable differences."
        elif avg_score >= 0.3:
            return "These strings have **low similarity** - they share only a few common elements."
        else:
            return "These strings are **very different** - they share minimal common elements."
    
    def _format_metric_explanation(self, metric: str, score: float,
                                   str1: str, str2: str) -> str:
        """Format explanation for a specific metric."""
        info = self.metric_descriptions[metric]
        
        # Determine interpretation level
        if score >= 0.7:
            level = 'high'
            emoji = '🟢'
        elif score >= 0.5:
            level = 'medium'
            emoji = '🟡'
        else:
            level = 'low'
            emoji = '🔴'
        
        explanation = f"### {emoji} {info['name']}: {score*100:.1f}%\n"
        explanation += f"*{info['description']}*\n\n"
        explanation += f"**What this means:** {info['interpretation'][level]}\n\n"
        
        # Add specific insights for semantic metric
        if metric == 'semantic':
            explanation += self._get_semantic_metric_insights(score, str1, str2)
        
        return explanation
    
    def _get_semantic_metric_insights(self, score: float, str1: str, str2: str) -> str:
        """Get specific insights for semantic metric."""
        insights = ""
        
        if score > 0.85:
            insights = "**Example interpretation:** Even if these texts use different words, an AI model recognizes they express the same ideas. For instance, 'The weather is pleasant today' and 'It's a nice day outside' would have high semantic similarity.\n\n"
        elif score > 0.6:
            insights = "**Example interpretation:** These texts discuss related topics. They might use some different words but the underlying subject matter overlaps significantly.\n\n"
        
        return insights
    
    def _get_specific_observations(self, scores: Dict[str, float],
                                   str1: str, str2: str) -> List[str]:
        """Generate specific observations about the strings."""
        observations = []
        
        # Length comparison
        len_diff = abs(len(str1) - len(str2))
        if len_diff == 0:
            observations.append("- Both strings have **exactly the same length**.")
        elif len_diff <= 5:
            observations.append(f"- String lengths differ by only **{len_diff} characters**.")
        else:
            observations.append(f"- String lengths differ by **{len_diff} characters**.")
        
        # Word count comparison
        words1 = len(str1.split())
        words2 = len(str2.split())
        if words1 == words2:
            observations.append("- Both strings have the **same number of words**.")
        
        # Semantic vs Lexical comparison
        if 'semantic' in scores and 'levenshtein' in scores:
            sem_score = scores['semantic']
            lex_score = scores['levenshtein']
            
            if sem_score > 0.7 and lex_score < 0.5:
                observations.append("- 🌟 **Interesting:** High semantic similarity but low character-level similarity! This suggests the texts are **paraphrases** - different words expressing the same meaning.")
            elif sem_score < 0.3 and lex_score > 0.7:
                observations.append("- ⚠️ **Note:** High character similarity but low semantic similarity. The texts might share similar spelling but discuss different topics.")
        
        return observations