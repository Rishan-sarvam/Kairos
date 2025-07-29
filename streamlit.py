import streamlit as st
import asyncio
import json
from typing import Dict, Any
import sys
import os

# Add the src directory to the path so we can import from main.py
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from kairos import run_evaluation

# Set page config
st.set_page_config(
    page_title="Web App Evaluation Framework",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .evaluation-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
    .result-container {
        background-color: #e8f4fd;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .sidebar .stSelectbox {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

async def run_async_evaluation(evaluation_type: str, user_query: str, url: str):
    """Wrapper function to run async evaluation functions"""
    try:
        if evaluation_type == "Qualitative Evaluation":
            return await run_evaluation(user_query, url, evaluation_type="qualitative")
        else:
            return await run_evaluation(user_query, url, evaluation_type="feature_correctness")
    except Exception as e:
        return f"Error during evaluation: {str(e)}"

def format_result(result: Any) -> str:
    """Format the evaluation result for display"""
    if isinstance(result, dict):
        return json.dumps(result, indent=2)
    elif isinstance(result, str):
        return result
    else:
        return str(result)

def main():
    # Sidebar
    with st.sidebar:
        st.title("🔍 Evaluation Settings")
        
        evaluation_type = st.selectbox(
            "Select Evaluation Type",
            ["Feature Correctness", "Qualitative Evaluation"],
            help="Choose the type of evaluation to perform on your web application"
        )
        
        st.markdown("---")
        
        # Information about evaluation types
        if evaluation_type == "Feature Correctness":
            st.info("""
            **Feature Correctness Evaluation**
            
            Tests specific functionality and features of the web application:
            - Creates detailed Playwright test plans
            - Verifies interactive elements work correctly
            - Checks forms, buttons, navigation, etc.
            - Provides structured test results
            """)
        else:
            st.info("""
            **Qualitative Evaluation**
            
            Performs a comprehensive quality assessment:
            - Overall user experience evaluation
            - Design and usability assessment
            - Performance and accessibility checks
            - Subjective quality metrics
            """)

    # Main content
    st.markdown('<h1 class="main-header">Web Application Evaluation Framework</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        user_query = st.text_area(
            "User Query",
            placeholder="Describe what your web application should do...",
            help="Provide a detailed description of your web application's intended functionality",
            height=150
        )
    
    with col2:
        generated_app_url = st.text_input(
            "Generated App URL",
            placeholder="https://your-app-url.com",
            help="Enter the URL of the web application you want to evaluate"
        )
        
        # URL validation
        if generated_app_url and not (generated_app_url.startswith('http://') or generated_app_url.startswith('https://')):
            st.warning("⚠️ Please enter a valid URL starting with http:// or https://")
    
    # Run evaluation button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Run Evaluation", type="primary", use_container_width=True):
            if not user_query.strip():
                st.error("❌ Please enter a user query")
            elif not generated_app_url.strip():
                st.error("❌ Please enter a valid URL")
            elif not (generated_app_url.startswith('http://') or generated_app_url.startswith('https://')):
                st.error("❌ Please enter a valid URL starting with http:// or https://")
            else:
                # Initialize session state for results if not exists
                if 'evaluation_results' not in st.session_state:
                    st.session_state.evaluation_results = []
                
                # Show progress
                with st.spinner(f'Running {evaluation_type}... This may take a few minutes.'):
                    try:
                        result = asyncio.run(run_async_evaluation(evaluation_type, user_query, generated_app_url))
                        
                        # Store result in session state
                        st.session_state.evaluation_results.append({
                            'type': evaluation_type,
                            'query': user_query,
                            'url': generated_app_url,
                            'result': result
                        })
                        
                        st.success("✅ Evaluation completed successfully!")
                        
                    except Exception as e:
                        st.error(f"❌ Error during evaluation: {str(e)}")

    # Results section
    if 'evaluation_results' in st.session_state and st.session_state.evaluation_results:
        st.markdown("---")
        st.subheader("📊 Evaluation Results")
        
        # Show most recent result first
        for i, eval_result in enumerate(reversed(st.session_state.evaluation_results)):
            with st.expander(f"🔍 {eval_result['type']} - Result {len(st.session_state.evaluation_results) - i}", expanded=(i == 0)):
                
                # Evaluation details
                st.markdown("**Evaluation Type:**")
                st.code(eval_result['type'])
                
                st.markdown("**User Query:**")
                st.text_area("Query", value=eval_result['query'], disabled=True, key=f"query_{i}")
                
                st.markdown("**URL:**")
                st.code(eval_result['url'])
                
                st.markdown("**Result:**")
                
                # Try to format JSON results nicely
                try:
                    if isinstance(eval_result['result'], str):
                        # Try to parse as JSON for better formatting
                        try:
                            json_result = json.loads(eval_result['result'])
                            st.json(json_result)
                        except:
                            st.text_area("Result", value=eval_result['result'], disabled=True, height=200, key=f"result_{i}")
                    else:
                        st.json(eval_result['result'])
                except:
                    st.text(str(eval_result['result']))
                
                # Download result button
                result_json = json.dumps(eval_result, indent=2, default=str)
                st.download_button(
                    label="📥 Download Result",
                    data=result_json,
                    file_name=f"evaluation_result_{eval_result['type'].lower().replace(' ', '_')}.json",
                    mime="application/json",
                    key=f"download_{i}"
                )

    # Clear results button
    if 'evaluation_results' in st.session_state and st.session_state.evaluation_results:
        if st.button("🗑️ Clear All Results", type="secondary"):
            st.session_state.evaluation_results = []
            st.rerun()

if __name__ == "__main__":
    main()
