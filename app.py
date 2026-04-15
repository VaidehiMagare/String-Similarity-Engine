# """Streamlit web application for string similarity engine."""

# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go
# from itertools import combinations

# from similarity import HybridSimilarity
# from preprocess.text_cleaning import TextCleaner
# from utils import format_score, interpret_score, get_score_color
# from explanation import ScoreExplainer


# # Page configuration
# st.set_page_config(
#     page_title="String Similarity Engine",
#     page_icon="📊",
#     layout="wide"
# )

# # Initialize components
# @st.cache_resource
# def get_components():
#     return {
#         'hybrid': HybridSimilarity(),
#         'cleaner': TextCleaner(),
#         'explainer': ScoreExplainer()
#     }

# components = get_components()


# # Custom CSS
# st.markdown("""
#     <style>
#     .main-header {
#         text-align: center;
#         padding: 20px;
#         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         border-radius: 10px;
#         margin-bottom: 30px;
#     }
#     .score-card {
#         padding: 20px;
#         border-radius: 10px;
#         background-color: #f8f9fa;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#         margin-bottom: 20px;
#     }
#     .metric-box {
#         padding: 15px;
#         border-radius: 8px;
#         background-color: white;
#         margin: 10px 0;
#         border-left: 4px solid #667eea;
#     }
#     </style>
# """, unsafe_allow_html=True)


# def create_score_gauge(score: float, title: str = "Similarity Score"):
#     """Create a gauge chart for similarity score."""
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number",
#         value=score * 100,
#         title={'text': title, 'font': {'size': 24}},
#         number={'suffix': "%", 'font': {'size': 40}},
#         gauge={
#             'axis': {'range': [0, 100], 'tickwidth': 1},
#             'bar': {'color': "#667eea"},
#             'steps': [
#                 {'range': [0, 30], 'color': "#ff6b6b"},
#                 {'range': [30, 50], 'color': "#ffd93d"},
#                 {'range': [50, 70], 'color': "#6bcf7f"},
#                 {'range': [70, 90], 'color': "#4d96ff"},
#                 {'range': [90, 100], 'color': "#6c5ce7"},
#             ],
#             'threshold': {
#                 'line': {'color': "red", 'width': 4},
#                 'thickness': 0.75,
#                 'value': score * 100
#             }
#         }
#     ))
    
#     fig.update_layout(
#         height=300,
#         margin=dict(l=30, r=30, t=50, b=30),
#         font={'size': 16}
#     )
    
#     return fig


# def create_comparison_matrix(strings):
#     """Create a similarity matrix for multiple strings."""
#     n = len(strings)
#     matrix = []
    
#     for i in range(n):
#         row = []
#         for j in range(n):
#             if i == j:
#                 row.append(1.0)
#             else:
#                 score = components['hybrid'].calculate_hybrid(strings[i], strings[j])
#                 row.append(score)
#         matrix.append(row)
    
#     return matrix


# def main():
#     """Main Streamlit application."""
    
#     # Header
#     st.markdown("""
#         <div class="main-header">
#             <h1>📊 String Similarity Engine</h1>
#             <p>Advanced text comparison using multiple similarity metrics</p>
#         </div>
#     """, unsafe_allow_html=True)
    
#     # Sidebar
#     with st.sidebar:
#         st.header("⚙️ Settings")
        
#         st.subheader("Preprocessing Options")
#         clean_text = st.checkbox("Clean text before comparison", value=True)
        
#         if clean_text:
#             lowercase = st.checkbox("Convert to lowercase", value=True)
#             remove_punct = st.checkbox("Remove punctuation", value=True)
#             remove_spaces = st.checkbox("Remove extra spaces", value=True)
        
#         st.subheader("Display Options")
#         show_all_metrics = st.checkbox("Show all metrics", value=True)
#         show_explanations = st.checkbox("Show detailed explanations", value=True)
        
#         st.markdown("---")
#         st.markdown("### 📚 About")
#         st.markdown("""
#         This engine compares strings using multiple similarity metrics:
#         - **Levenshtein**: Character-level edits
#         - **Jaccard**: Word set overlap
#         - **Cosine**: Word frequency patterns
#         - **Overlap**: Content coverage
#         - **Sequence**: Common subsequences
#         """)
    
#     # Main content area
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         st.header("📝 Input Strings")
        
#         # Initialize session state for string inputs
#         if 'string_inputs' not in st.session_state:
#             st.session_state.string_inputs = ['', '']
        
#         # Dynamic string inputs
#         num_inputs = len(st.session_state.string_inputs)
        
#         for i in range(num_inputs):
#             col_input, col_button = st.columns([5, 1])
#             with col_input:
#                 st.session_state.string_inputs[i] = st.text_area(
#                     f"String {i+1}",
#                     value=st.session_state.string_inputs[i],
#                     height=100,
#                     key=f"string_{i}"
#                 )
#             with col_button:
#                 if i >= 2 and st.button("❌", key=f"remove_{i}"):
#                     st.session_state.string_inputs.pop(i)
#                     st.rerun()
        
#         # Add more strings button
#         if st.button("➕ Add Another String"):
#             st.session_state.string_inputs.append('')
#             st.rerun()
        
#         # Compare button
#         compare_button = st.button("🔍 Compare Strings", type="primary", use_container_width=True)
    
#     # Results section
#     if compare_button:
#         # Filter out empty strings
#         valid_strings = [s for s in st.session_state.string_inputs if s.strip()]
        
#         if len(valid_strings) < 2:
#             st.warning("⚠️ Please enter at least two non-empty strings to compare.")
#             return
        
#         st.markdown("---")
#         st.header("📈 Results")
        
#         # Preprocess if needed
#         if clean_text:
#             processed_strings = []
#             for s in valid_strings:
#                 cleaned = s
#                 if lowercase:
#                     cleaned = cleaned.lower()
#                 if remove_punct:
#                     import string
#                     cleaned = cleaned.translate(str.maketrans('', '', string.punctuation))
#                 if remove_spaces:
#                     import re
#                     cleaned = re.sub(r'\s+', ' ', cleaned).strip()
#                 processed_strings.append(cleaned)
#         else:
#             processed_strings = valid_strings
        
#         if len(valid_strings) == 2:
#             # Two-string comparison
#             str1, str2 = processed_strings[0], processed_strings[1]
            
#             # Calculate all scores
#             scores = components['hybrid'].calculate_all(str1, str2)
#             hybrid_score = components['hybrid'].calculate_hybrid(str1, str2)
            
#             with col2:
#                 st.markdown("### 🎯 Overall Score")
#                 category, description = interpret_score(hybrid_score)
#                 color = get_score_color(hybrid_score)
                
#                 fig = create_score_gauge(hybrid_score, "Hybrid Similarity Score")
#                 st.plotly_chart(fig, use_container_width=True)
                
#                 st.markdown(f"""
#                     <div class="score-card">
#                         <h3>{color} {category}</h3>
#                         <p>{description}</p>
#                         <h2 style="color: #667eea;">{format_score(hybrid_score)}</h2>
#                     </div>
#                 """, unsafe_allow_html=True)
            
#             if show_all_metrics:
#                 st.markdown("### 📊 Detailed Metrics")
                
#                 # Create metrics grid
#                 cols = st.columns(3)
#                 metrics_list = list(scores.items())
                
#                 for i, (metric, score) in enumerate(metrics_list):
#                     with cols[i % 3]:
#                         color = get_score_color(score)
#                         st.markdown(f"""
#                             <div class="metric-box">
#                                 <h4>{color} {metric.replace('_', ' ').title()}</h4>
#                                 <h3>{format_score(score)}</h3>
#                             </div>
#                         """, unsafe_allow_html=True)
            
#             if show_explanations:
#                 st.markdown("### 💡 Similarity Analysis")
#                 explanation = components['explainer'].generate_explanation(
#                     scores, str1, str2
#                 )
#                 st.markdown(explanation)
        
#         else:
#             # Multiple string comparison
#             st.markdown("### 🔄 Multiple String Comparison")
            
#             # Create comparison matrix
#             matrix = create_comparison_matrix(processed_strings)
#             df_matrix = pd.DataFrame(
#                 matrix,
#                 columns=[f"S{i+1}" for i in range(len(valid_strings))],
#                 index=[f"S{i+1}" for i in range(len(valid_strings))]
#             )
            
#             # Display heatmap
#             fig = go.Figure(data=go.Heatmap(
#                 z=matrix,
#                 x=[f"String {i+1}" for i in range(len(valid_strings))],
#                 y=[f"String {i+1}" for i in range(len(valid_strings))],
#                 colorscale='Viridis',
#                 zmin=0,
#                 zmax=1,
#                 text=[[f"{val*100:.1f}%" for val in row] for row in matrix],
#                 texttemplate='%{text}',
#                 textfont={"size": 12},
#                 hoverongaps=False
#             ))
            
#             fig.update_layout(
#                 title="Similarity Matrix",
#                 height=500,
#                 xaxis_title="Strings",
#                 yaxis_title="Strings"
#             )
            
#             st.plotly_chart(fig, use_container_width=True)
            
#             # Show pairwise comparisons
#             st.markdown("### 📋 Pairwise Comparisons")
            
#             for i, j in combinations(range(len(valid_strings)), 2):
#                 with st.expander(f"String {i+1} vs String {j+1}"):
#                     score = components['hybrid'].calculate_hybrid(
#                         processed_strings[i], processed_strings[j]
#                     )
#                     category, _ = interpret_score(score)
#                     color = get_score_color(score)
                    
#                     st.markdown(f"""
#                         **Similarity Score:** {color} {format_score(score)} ({category})
#                     """)
                    
#                     st.text(f"String {i+1}: {valid_strings[i][:100]}...")
#                     st.text(f"String {j+1}: {valid_strings[j][:100]}...")
                    
#                     # Show detailed scores
#                     scores = components['hybrid'].calculate_all(
#                         processed_strings[i], processed_strings[j]
#                     )
                    
#                     score_df = pd.DataFrame({
#                         'Metric': scores.keys(),
#                         'Score': [format_score(s) for s in scores.values()]
#                     })
#                     st.dataframe(score_df, use_container_width=True)


# if __name__ == "__main__":
#     main()

"""Streamlit web application for string similarity engine with semantic analysis."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from itertools import combinations
import re
import string

from similarity import HybridSimilarity
from preprocess.text_cleaning import TextCleaner
from utils import format_score, interpret_score, get_score_color
from explanation import ScoreExplainer


# Page configuration
st.set_page_config(
    page_title="String Similarity Engine",
    page_icon="📊",
    layout="wide"
)

# Initialize components with caching
@st.cache_resource
def get_components():
    """Initialize and cache heavy components."""
    try:
        hybrid = HybridSimilarity(use_semantic=True)
    except Exception as e:
        st.warning(f"Semantic similarity not available: {e}. Using lexical metrics only.")
        hybrid = HybridSimilarity(use_semantic=False)
    
    return {
        'hybrid': hybrid,
        'cleaner': TextCleaner(),
        'explainer': ScoreExplainer()
    }

# Load components at startup
components = get_components()


# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .score-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f8f9fa;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .metric-box {
        padding: 15px;
        border-radius: 8px;
        background-color: white;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    .semantic-highlight {
        border-left: 4px solid #28a745;
        background: linear-gradient(90deg, #f0fff4 0%, #ffffff 100%);
    }
    </style>
""", unsafe_allow_html=True)


def create_score_gauge(score: float, title: str = "Similarity Score"):
    """Create a gauge chart for similarity score."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score * 100,
        title={'text': title, 'font': {'size': 24}},
        number={'suffix': "%", 'font': {'size': 40}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': "#667eea"},
            'steps': [
                {'range': [0, 30], 'color': "#ff6b6b"},
                {'range': [30, 50], 'color': "#ffd93d"},
                {'range': [50, 70], 'color': "#6bcf7f"},
                {'range': [70, 90], 'color': "#4d96ff"},
                {'range': [90, 100], 'color': "#6c5ce7"},
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': score * 100
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=30, r=30, t=50, b=30),
        font={'size': 16}
    )
    
    return fig


def create_comparison_matrix(strings):
    """Create a similarity matrix for multiple strings."""
    n = len(strings)
    matrix = []
    
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(1.0)
            else:
                score = components['hybrid'].calculate_hybrid(strings[i], strings[j])
                row.append(score)
        matrix.append(row)
    
    return matrix


def display_semantic_analysis(scores, str1, str2):
    """Display semantic similarity analysis."""
    if 'semantic' in scores:
        semantic_score = scores['semantic']
        
        st.markdown("### 🧠 Semantic (Meaning-Based) Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            color = get_score_color(semantic_score)
            st.markdown(f"""
                <div class="metric-box semantic-highlight">
                    <h4>{color} Semantic Similarity</h4>
                    <h3>{format_score(semantic_score)}</h3>
                    <p><small>Measures how similar the meanings are, regardless of exact wording</small></p>
                </div>
            """, unsafe_allow_html=True)
            
            # Semantic interpretation
            if semantic_score >= 0.85:
                st.success("✅ **Excellent meaning match!** These texts express the same ideas.")
            elif semantic_score >= 0.70:
                st.success("🟢 **Good meaning match!** The texts share very similar concepts.")
            elif semantic_score >= 0.50:
                st.info("🟡 **Moderate meaning match.** Some shared concepts but different expression.")
            elif semantic_score >= 0.30:
                st.warning("🟠 **Weak meaning match.** Limited conceptual overlap.")
            else:
                st.error("🔴 **Different meanings.** These texts discuss different topics.")
        
        with col2:
            # Compare semantic vs lexical
            if 'levenshtein' in scores:
                lex_score = scores['levenshtein']
                
                if semantic_score > 0.7 and lex_score < 0.5:
                    st.markdown("""
                    <div class="insight-box">
                        <h4>🌟 Paraphrase Detected!</h4>
                        <p>High semantic similarity but different wording suggests these are paraphrases - different words expressing the same meaning.</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif semantic_score < 0.3 and lex_score > 0.7:
                    st.markdown("""
                    <div class="insight-box">
                        <h4>⚠️ Different Topics, Similar Words</h4>
                        <p>High character similarity but low semantic similarity suggests different topics using similar vocabulary.</p>
                    </div>
                    """, unsafe_allow_html=True)


def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>📊 String Similarity Engine</h1>
            <p>Advanced text comparison using multiple similarity metrics including semantic analysis</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        st.subheader("Preprocessing Options")
        clean_text = st.checkbox("Clean text before comparison", value=True)
        
        if clean_text:
            lowercase = st.checkbox("Convert to lowercase", value=True)
            remove_punct = st.checkbox("Remove punctuation", value=True)
            remove_spaces = st.checkbox("Remove extra spaces", value=True)
        
        st.subheader("Display Options")
        show_all_metrics = st.checkbox("Show all metrics", value=True)
        show_explanations = st.checkbox("Show detailed explanations", value=True)
        show_semantic = st.checkbox("Show semantic analysis", value=True)
        
        st.markdown("---")
        st.markdown("### 📚 About")
        st.markdown("""
        This engine compares strings using multiple similarity metrics:
        - **Levenshtein**: Character-level edits
        - **Jaccard**: Word set overlap
        - **Cosine**: Word frequency patterns
        - **Overlap**: Content coverage
        - **Sequence**: Common subsequences
        - **Semantic**: Meaning-based similarity (AI)
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Input Strings")
        
        # Initialize session state for string inputs
        if 'string_inputs' not in st.session_state:
            st.session_state.string_inputs = ['', '']
        
        # Dynamic string inputs
        num_inputs = len(st.session_state.string_inputs)
        
        for i in range(num_inputs):
            col_input, col_button = st.columns([5, 1])
            with col_input:
                st.session_state.string_inputs[i] = st.text_area(
                    f"String {i+1}",
                    value=st.session_state.string_inputs[i],
                    height=100,
                    key=f"string_{i}"
                )
            with col_button:
                if i >= 2 and st.button("❌", key=f"remove_{i}"):
                    st.session_state.string_inputs.pop(i)
                    st.rerun()
        
        # Add more strings button
        if st.button("➕ Add Another String"):
            st.session_state.string_inputs.append('')
            st.rerun()
        
        # Compare button
        compare_button = st.button("🔍 Compare Strings", type="primary", use_container_width=True)
    
    # Results section
    if compare_button:
        # Filter out empty strings
        valid_strings = [s for s in st.session_state.string_inputs if s.strip()]
        
        if len(valid_strings) < 2:
            st.warning("⚠️ Please enter at least two non-empty strings to compare.")
            return
        
        st.markdown("---")
        st.header("📈 Results")
        
        # Preprocess if needed
        if clean_text:
            processed_strings = []
            for s in valid_strings:
                cleaned = s
                if lowercase:
                    cleaned = cleaned.lower()
                if remove_punct:
                    cleaned = cleaned.translate(str.maketrans('', '', string.punctuation))
                if remove_spaces:
                    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
                processed_strings.append(cleaned)
        else:
            processed_strings = valid_strings
        
        if len(valid_strings) == 2:
            # Two-string comparison
            str1, str2 = processed_strings[0], processed_strings[1]
            original_str1, original_str2 = valid_strings[0], valid_strings[1]
            
            # Calculate all scores
            with st.spinner("Calculating similarities..."):
                scores = components['hybrid'].calculate_all(original_str1, original_str2, clean=False)
                hybrid_score = components['hybrid'].calculate_hybrid(original_str1, original_str2, clean=False)
            
            with col2:
                st.markdown("### 🎯 Overall Score")
                category, description = interpret_score(hybrid_score)
                color = get_score_color(hybrid_score)
                
                fig = create_score_gauge(hybrid_score, "Hybrid Similarity Score")
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown(f"""
                    <div class="score-card">
                        <h3>{color} {category}</h3>
                        <p>{description}</p>
                        <h2 style="color: #667eea;">{format_score(hybrid_score)}</h2>
                    </div>
                """, unsafe_allow_html=True)
            
            # Display semantic analysis if enabled
            if show_semantic and 'semantic' in scores:
                st.markdown("---")
                display_semantic_analysis(scores, original_str1, original_str2)
            
            if show_all_metrics:
                st.markdown("### 📊 Detailed Metrics")
                
                # Create metrics grid
                cols = st.columns(3)
                metrics_list = list(scores.items())
                
                for i, (metric, score) in enumerate(metrics_list):
                    with cols[i % 3]:
                        color = get_score_color(score)
                        # Add special class for semantic metric
                        special_class = "semantic-highlight" if metric == 'semantic' else ""
                        st.markdown(f"""
                            <div class="metric-box {special_class}">
                                <h4>{color} {metric.replace('_', ' ').title()}</h4>
                                <h3>{format_score(score)}</h3>
                            </div>
                        """, unsafe_allow_html=True)
            
            if show_explanations:
                st.markdown("### 💡 Similarity Analysis")
                
                # Get breakdown for better explanation
                try:
                    breakdown = components['hybrid'].get_similarity_breakdown(original_str1, original_str2)
                    explanation = components['explainer'].generate_explanation(
                        scores, original_str1, original_str2, breakdown
                    )
                except:
                    explanation = components['explainer'].generate_explanation(
                        scores, original_str1, original_str2
                    )
                
                st.markdown(explanation)
        
        else:
            # Multiple string comparison
            st.markdown("### 🔄 Multiple String Comparison")
            
            with st.spinner("Calculating similarity matrix..."):
                # Create comparison matrix
                matrix = create_comparison_matrix(processed_strings)
                df_matrix = pd.DataFrame(
                    matrix,
                    columns=[f"S{i+1}" for i in range(len(valid_strings))],
                    index=[f"S{i+1}" for i in range(len(valid_strings))]
                )
            
            # Display heatmap
            fig = go.Figure(data=go.Heatmap(
                z=matrix,
                x=[f"String {i+1}" for i in range(len(valid_strings))],
                y=[f"String {i+1}" for i in range(len(valid_strings))],
                colorscale='Viridis',
                zmin=0,
                zmax=1,
                text=[[f"{val*100:.1f}%" for val in row] for row in matrix],
                texttemplate='%{text}',
                textfont={"size": 12},
                hoverongaps=False
            ))
            
            fig.update_layout(
                title="Similarity Matrix",
                height=500,
                xaxis_title="Strings",
                yaxis_title="Strings"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show pairwise comparisons
            st.markdown("### 📋 Pairwise Comparisons")
            
            for i, j in combinations(range(len(valid_strings)), 2):
                with st.expander(f"String {i+1} vs String {j+1}"):
                    score = components['hybrid'].calculate_hybrid(
                        valid_strings[i], valid_strings[j], clean=False
                    )
                    category, _ = interpret_score(score)
                    color = get_score_color(score)
                    
                    st.markdown(f"""
                        **Similarity Score:** {color} {format_score(score)} ({category})
                    """)
                    
                    st.text(f"String {i+1}: {valid_strings[i][:100]}...")
                    st.text(f"String {j+1}: {valid_strings[j][:100]}...")
                    
                    # Show detailed scores
                    scores = components['hybrid'].calculate_all(
                        valid_strings[i], valid_strings[j], clean=False
                    )
                    
                    score_df = pd.DataFrame({
                        'Metric': scores.keys(),
                        'Score': [format_score(s) for s in scores.values()]
                    })
                    st.dataframe(score_df, use_container_width=True)


if __name__ == "__main__":
    main()