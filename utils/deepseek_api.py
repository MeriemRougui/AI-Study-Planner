# utils/deepseek_api.py - WORKING VERSION
import streamlit as st
from openai import OpenAI
import os

def get_deepseek_client():
    """Initialize DeepSeek API client"""
    try:
        api_key = st.secrets.get("DEEPSEEK_API_KEY", "").strip()
        
        if not api_key:
            st.error("❌ No API key found in secrets.toml")
            return None
        
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com",
            timeout=30.0
        )
        return client
        
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None

def generate_study_plan(user_query, max_tokens=500):
    """Generate study plan using DeepSeek API"""
    client = get_deepseek_client()
    
    if not client:
        return "Error: Could not initialize API client"
    
    system_prompt = """You are an expert AI Study Assistant specialized in creating study routines.
    
    CRITICAL RULES:
    1. ALWAYS respond in bullet points
    2. Use • for each bullet
    3. Include specific time allocations (e.g., "5-30 min:")
    4. Structure: Preparation → Study Blocks → Breaks → Tips
    5. NO paragraphs, NO explanations, JUST bullet points
    
    EXAMPLE:
    • 0-5 min: Prepare workspace
    • 5-30 min: Focus on main topic
    • 30-35 min: Break - stretch
    • 35-60 min: Practice exercises"""
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{user_query}\n\nRespond ONLY in bullet points with time allocations."}
            ],
            max_tokens=max_tokens,
            temperature=0.3,
        )
        
        # Log usage (optional)
        tokens = response.usage.total_tokens
        cost = tokens * 0.14 / 1_000_000  # Cost in yuan
        print(f"📊 Used {tokens} tokens, cost: {cost:.8f} yuan")
        
        return response.choices[0].message.content
        
    except Exception as e:
        st.error(f"❌ API Error: {e}")
        return f"Error: {str(e)[:100]}"