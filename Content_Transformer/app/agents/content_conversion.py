import logging
from typing import TypedDict, Dict, Any, Optional
from llm_client import call_llm
from rag.retriveal import retrieve_style_examples

# Configure logging
logger = logging.getLogger(__name__)

class ContentState(TypedDict):
    input_content: str
    transformation_plan: str
    user_preferences: Dict[str, Any]
    user_suggestions: Optional[str]
    converted_output: str

def content_conversion_agent(state: ContentState) -> ContentState:
    user_suggestions = state.get("user_suggestions")
    user_preferences = state.get("user_preferences", {})
    
    # Retrieve relevant style examples and transformation cases
    target_format = user_preferences.get("target_format", "auto")
    target_tone = user_preferences.get("tone", "auto")
    target_complexity = user_preferences.get("complexity", "auto")
    
    # Create query for retrieval based on transformation requirements
    # Find examples of the target format and tone (more flexible matching)
    retrieval_query = f"{target_format} {target_tone}"
    
    # Log the query for debugging
    logger.info(f"RAG QUERY: Looking for {target_format} examples with {target_tone} tone")
    
    # Get relevant examples from knowledge base
    style_examples = retrieve_style_examples(retrieval_query, n_results=5)
    
    # Log all 5 matches for debugging
    logger.info(f"RAG SEARCH RESULTS ({len(style_examples)} matches):")
    logger.info("-" * 50)
    for i, example in enumerate(style_examples, 1):
        logger.info(f"Match {i}: {example[:100]}...")
    logger.info("-" * 50)
    
    # Build examples context for the prompt
    examples_context = ""
    if style_examples:
        examples_context = f"""
        
        RELEVANT STYLE EXAMPLES AND TRANSFORMATION CASES:
        {chr(10).join([f"Example {i+1}: {example}" for i, example in enumerate(style_examples)])}
        
        Use these examples as reference for the target style, format, and tone. 
        Adapt the patterns and techniques shown in these examples to guide your transformation.
        """
    else:
        examples_context = """
        
        No specific style examples found. Proceed with standard transformation principles.
        """
    
    # Build the prompt with user suggestions if available
    suggestions_context = ""
    if user_suggestions:
        suggestions_context = f"""
        
        USER SUGGESTIONS FOR IMPROVEMENT:
        {user_suggestions}
        
        Please pay special attention to these suggestions when executing the transformation.
        """
    
    prompt = f"""You are a Content Conversion Agent specialized in transforming content between different formats, styles, and complexity levels.
        
        Your task is to execute content transformations based on detailed plans and analysis. You must:
        
        1. PRESERVE the core meaning and key information from the original content
        2. ADAPT the format, style, and complexity according to specifications
        3. MAINTAIN coherence and readability throughout the transformation
        4. FOLLOW the transformation plan step by step
        5. ENSURE the output meets the target format requirements
        6. ADDRESS any user suggestions for improvement
        7. USE the provided style examples as reference for target format and tone
        
        Key transformation principles:
        - Format conversion: Adapt structure, tone, and presentation style
        - Complexity adjustment: Modify vocabulary, sentence structure, and technical depth
        - Style adaptation: Change tone, formality, and engagement level
        - Content preservation: Maintain essential information and key points
        - User feedback incorporation: Address specific user concerns and suggestions
        - Example-based learning: Apply patterns from similar transformations
        
        {examples_context}
        {suggestions_context}
        
        Provide the transformed content directly without additional explanations or formatting.
        Focus on producing high-quality, well-structured output that meets all specified requirements.
        If user suggestions are provided, make sure to address them in your transformation.
        Use the style examples as guidance for achieving the target format and tone.
        
        Original Content to Transform:
        {state['input_content']}
        
        Transformation Plan to Follow:
        {state['transformation_plan']}"""
    
    converted = call_llm(prompt)
    return {**state, "converted_output": converted}
