# pages/ai_assistant.py - FIXED VERSION
import streamlit as st
from utils.deepseek_api import generate_study_plan

def show_ai_assistant():
    st.title("🤖 AI Study Assistant")
    st.write("Ask for help with study plans, summaries, tips, anything! 💛")
    
    # Quick templates
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📚 3-Hour Routine", use_container_width=True):
            st.session_state.query = "Create a 3-hour distraction-free study routine"
    
    with col2:
        if st.button("⏰ 2-Hour Plan", use_container_width=True):
            st.session_state.query = "Make a 2-hour study schedule with breaks"
    
    with col3:
        if st.button("🎯 Focus Tips", use_container_width=True):
            st.session_state.query = "Give bullet-point tips for staying focused"
    
    # User input
    if "query" in st.session_state:
        user_input = st.text_area("Your question:", value=st.session_state.query, height=100)
        del st.session_state.query
    else:
        user_input = st.text_area("Your question:", placeholder="Example: Create a study plan for...", height=100)
    
    if st.button("✨ Generate Study Plan", type="primary"):
        if not user_input.strip():
            st.warning("Please enter a question! 🤭")
        else:
            with st.spinner("🧠 AI is creating your perfect study plan..."):
                response = generate_study_plan(user_input)
                
                st.success("✨ Your AI-Generated Study Plan:")
                
                # FIXED: Clean formatting
                cleaned_response = response.replace('<br>', '').replace('<br/>', '')
                
                # Display with nice formatting
                st.markdown(f"""
                <div style="
                    background-color: #f0f9ff;
                    border-left: 5px solid #3b82f6;
                    padding: 25px;
                    border-radius: 12px;
                    margin: 20px 0;
                    line-height: 1.8;
                    font-size: 16px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                ">
                {cleaned_response.replace('\\n', '<br>')}
                </div>
                """, unsafe_allow_html=True)
                
                # Also show as plain text for copying
                with st.expander("📋 Copy this plan"):
                    st.code(response, language="markdown")