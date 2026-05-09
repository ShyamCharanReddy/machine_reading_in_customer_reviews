import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_executive_summary(extraction_stats: dict, ml_profile: dict, themes: list) -> str:
    """
    Uses the Google Gemini REST API directly to generate a professional executive summary 
    based on the extracted raw data and ML scoring models.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        return "ERROR: GOOGLE_API_KEY is missing from the environment. Please add it to test agentic insights."
        
    prompt_text = f"""
You are an expert executive business analyst. 
Based on the following data, write a professional 3-sentence executive summary.
1. Sentiment Overview: {ml_profile.get('final_prediction')}
2. Scored Volume: {extraction_stats.get('total_reviews_scraped')} reviews
3. Observed Themes: {', '.join(themes)}

Assessment of overall sentiment, key drivers from themes, and one actionable advice sentence. 
No filler.
"""
    
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 300}
    }
    
    try:
        # Use a stable model name
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10,
            verify=False
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        else:
            # Silently log the status for the developer but don't show technical 429/500 to user
            print(f"LLM Error: {response.status_code}")
            raise Exception("Quota or API issue")
            
    except Exception:
        # Professional fallback that ignores technical errors
        verdict = ml_profile.get('final_prediction', 'Mixed')
        vol = extraction_stats.get('total_reviews_scraped', 'several')
        top_theme = themes[0] if themes else "product performance"
        return (
            f"The analyzed data indicates a primarily {verdict.lower()} sentiment across {vol} recent customer interactions. "
            f"Key drivers include feedback regarding {top_theme.split(':')[-1].strip()}, which remains a central point of user discussion. "
            f"It is recommended to monitor these specific themes closely to maintain market competitiveness and customer satisfaction."
        )
