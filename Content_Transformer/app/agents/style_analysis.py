from typing import TypedDict, Dict, Any
from llm_client import call_llm

class ContentState(TypedDict):
    input_content: str
    user_preferences: Dict[str, Any]
    analysis: str

def style_analysis_agent(state: ContentState) -> ContentState:
    preferences = state.get("user_preferences", {})
    target_format = preferences.get("target_format", "auto")
    target_complexity = preferences.get("complexity", "auto")
    target_tone = preferences.get("tone", "auto")
    
    prompt = f"""You are a Style Analysis Agent specialized in analyzing content characteristics and style patterns.
        
        Your task is to analyze the given content and extract detailed style characteristics including:
        - Current tone (formal, casual, professional, friendly, authoritative)
        - Complexity level (simplified, standard, advanced, expert)
        - Structure type (narrative, technical, persuasive, informative, etc.)
        - Key characteristics (engaging, technical, persuasive, etc.)
        - Target audience (general, technical, academic, business, etc.)
        - Content length category (short, medium, long)
        - Technical depth (minimal, moderate, detailed, comprehensive)
        - Content type (article, email, report, blog, etc.)
        
        User Preferences:
        - Target Format: {target_format}
        - Target Complexity: {target_complexity}
        - Target Tone: {target_tone}
        
        Provide your analysis in JSON format with the following structure:
        {{
            "current_tone": "string",
            "complexity_level": "string", 
            "structure_type": "string",
            "key_characteristics": ["string"],
            "target_audience": "string",
            "content_length": "string",
            "technical_depth": "string",
            "content_type": "string",
            "transformation_gap": {{
                "tone_gap": "string",
                "complexity_gap": "string",
                "format_gap": "string"
            }}
        }}
        
        Be precise and objective in your analysis. Consider the content type, vocabulary level, sentence structure, and overall style patterns.
        Also analyze the gap between current content characteristics and user preferences.
        
        Content to analyze:
        {state['input_content']}"""
    
    analysis = call_llm(prompt)
    return {**state, "analysis": analysis}
