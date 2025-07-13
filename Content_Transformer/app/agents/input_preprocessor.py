from typing import TypedDict, Dict, Any, Optional
from llm_client import call_llm

class ContentState(TypedDict):
    raw_input: str
    input_content: str
    user_preferences: Dict[str, Any]
    user_suggestions: Optional[str]
    analysis: str
    transformation_plan: str
    converted_output: str
    final_output: str

def input_preprocessor_agent(state: ContentState) -> ContentState:
    """
    Preprocesses user input to extract content and determine transformation preferences.
    This agent acts as the entry point and converts various input formats into structured data.
    """
    
    raw_input = state.get("raw_input", "")
    
    prompt = f"""You are an Input Preprocessing Agent that converts user input into structured content and preferences for content transformation.

    Your task is to:
    1. Extract the main content from the input
    2. Identify the current format/type of the content
    3. Determine the target format based on user intent or content analysis
    4. Set appropriate transformation preferences
    5. Clean and prepare the content for analysis

    Input to process:
    {raw_input}

    Analyze the input and provide your response in JSON format with the following structure:
    {{
        "extracted_content": "The main content extracted from the input",
        "current_format": "email|report|article|blog|technical|academic|marketing|other",
        "target_format": "blog|report|article|email|casual|professional|technical|simple",
        "target_complexity": "simple|standard|advanced|auto",
        "target_tone": "formal|casual|professional|friendly|auto",
        "transformation_reason": "Brief explanation of why this transformation is needed",
        "key_improvements": ["List of specific improvements needed"]
    }}

    Guidelines for analysis:
    - If input is an email, consider converting to a report or blog format
    - If input is formal/technical, consider making it more casual/accessible
    - If input is long/complex, consider simplifying it
    - If input lacks structure, consider organizing it better
    - Focus on making content more engaging and readable
    - Preserve all important information while improving presentation

    Be intelligent about format detection and target selection. Consider the content's purpose and audience.
    """
    
    try:
        response = call_llm(prompt)
        
        # Parse the JSON response (in a real implementation, you'd use json.loads)
        # For now, we'll extract the key information manually
        import json
        try:
            parsed_response = json.loads(response)
        except:
            # Fallback parsing if JSON is malformed
            parsed_response = {
                "extracted_content": raw_input,
                "current_format": "other",
                "target_format": "blog",
                "target_complexity": "simple",
                "target_tone": "casual",
                "transformation_reason": "Convert to more accessible format",
                "key_improvements": ["Make language simpler", "Improve structure", "Enhance readability"]
            }
        
        # Extract the processed data
        extracted_content = parsed_response.get("extracted_content", raw_input)
        current_format = parsed_response.get("current_format", "other")
        target_format = parsed_response.get("target_format", "blog")
        target_complexity = parsed_response.get("target_complexity", "simple")
        target_tone = parsed_response.get("target_tone", "casual")
        transformation_reason = parsed_response.get("transformation_reason", "Improve readability")
        key_improvements = parsed_response.get("key_improvements", [])
        
        # Create user preferences
        user_preferences = {
            "target_format": target_format,
            "complexity": target_complexity,
            "tone": target_tone,
            "current_format": current_format,
            "transformation_reason": transformation_reason,
            "key_improvements": key_improvements
        }
        
        # Create user suggestions based on key improvements
        user_suggestions = "; ".join(key_improvements) if key_improvements else None
        
        return {
            **state,
            "input_content": extracted_content,
            "user_preferences": user_preferences,
            "user_suggestions": user_suggestions
        }
        
    except Exception as e:
        # Fallback in case of errors
        return {
            **state,
            "input_content": raw_input,
            "user_preferences": {
                "target_format": "blog",
                "complexity": "simple",
                "tone": "casual",
                "current_format": "other",
                "transformation_reason": "Improve readability",
                "key_improvements": ["Make content more accessible"]
            },
            "user_suggestions": "Make content more accessible and engaging"
        } 