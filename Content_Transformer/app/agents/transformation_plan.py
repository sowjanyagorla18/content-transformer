from typing import TypedDict, Dict, Any, Optional
from llm_client import call_llm

class ContentState(TypedDict):
    analysis: str
    user_preferences: Dict[str, Any]
    user_suggestions: Optional[str]
    transformation_plan: str

def transformation_planning_agent(state: ContentState) -> ContentState:
    preferences = state.get("user_preferences", {})
    user_suggestions = state.get("user_suggestions")
    
    # Build the prompt with user suggestions if available
    suggestions_context = ""
    if user_suggestions:
        suggestions_context = f"""
        
        USER SUGGESTIONS FOR IMPROVEMENT:
        {user_suggestions}
        
        Please incorporate these suggestions into your transformation plan to address the user's concerns.
        """
    
    prompt = f"""You are a Transformation Planning Agent specialized in designing content conversion strategies.
        
        Your task is to create a detailed transformation plan that includes:
        - Specific transformation steps with clear instructions
        - Overall strategy for the transformation
        - Estimated difficulty level
        - Key changes to be made
        - Quality checkpoints during the process
        
        Consider the following transformation aspects:
        1. Format conversion (article to blog, technical to general, etc.)
        2. Complexity adjustment (simplify or enhance)
        3. Style adaptation (tone, length, structure)
        4. Content preservation (key points, accuracy)
        
        {suggestions_context}
        
        Provide your plan in JSON format with the following structure:
        {{
            "steps": [
                {{
                    "step_number": 1,
                    "action": "string",
                    "description": "string",
                    "expected_outcome": "string"
                }}
            ],
            "strategy": "string",
            "estimated_difficulty": "string",
            "key_changes": ["string"],
            "quality_checkpoints": ["string"],
            "improvement_focus": "string"
        }}
        
        Be specific and actionable in your planning. Consider the source and target formats, complexity requirements, and style preferences.
        If user suggestions are provided, prioritize addressing those specific concerns in your plan.
        
        Based on this style analysis:
        {state['analysis']}"""
    
    plan = call_llm(prompt)
    return {**state, "transformation_plan": plan}