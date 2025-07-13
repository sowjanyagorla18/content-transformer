from typing import TypedDict, Dict, Any
from llm_client import call_llm
from fact_checker import fact_check_transformation

class ContentState(TypedDict):
    input_content: str
    converted_output: str
    final_output: str

def quality_control_agent(state: ContentState) -> ContentState:
    # Perform fact checking
    fact_check_report = fact_check_transformation(
        state.get("input_content", ""), 
        state.get("converted_output", "")
    )
    
    # Build fact checking context
    fact_context = f"""
    
    FACT CHECKING RESULTS:
    - Preservation Score: {fact_check_report.get('preservation_score', 0.0)}
    - Original Facts Count: {fact_check_report.get('original_facts_count', 0)}
    - Preserved Facts: {len(fact_check_report.get('preserved_facts', []))}
    - Missing Facts: {len(fact_check_report.get('missing_facts', []))}
    - Fact Quality: {fact_check_report.get('overall_fact_quality', 'unknown')}
    - Accuracy Assessment: {fact_check_report.get('accuracy_assessment', 'Not available')}
    """
    
    if fact_check_report.get('improvement_suggestions'):
        fact_context += f"\n- Improvement Suggestions: {fact_check_report.get('improvement_suggestions')}"
    
    prompt = f"""You are a Quality Control Agent specialized in evaluating content transformation quality.
        
        Your task is to assess the quality of transformed content across multiple dimensions:
        
        1. READABILITY (0-1): How easy is the content to read and understand?
        2. COHERENCE (0-1): How well does the content flow and connect logically?
        3. ACCURACY (0-1): How accurately does the transformed content preserve the original meaning?
        4. STYLE CONSISTENCY (0-1): How consistent is the style throughout the content?
        5. CONTENT PRESERVATION (0-1): How well are key points and information preserved?
        6. FACTUAL ACCURACY (0-1): How well are facts preserved and verified?
        7. ENGAGEMENT (0-1): How engaging and compelling is the content?
        8. FORMAT ADHERENCE (0-1): How well does the content match the target format?
        
        Calculate an OVERALL SCORE (0-1) as the weighted average of all metrics.
        
        {fact_context}
        
        Provide your evaluation in JSON format with the following structure:
        {{
            "readability_score": 0.85,
            "coherence_score": 0.90,
            "accuracy_score": 0.95,
            "style_consistency_score": 0.88,
            "content_preservation_score": 0.92,
            "factual_accuracy_score": 0.87,
            "engagement_score": 0.83,
            "format_adherence_score": 0.91,
            "overall_score": 0.89,
            "fact_check_summary": {{
                "preservation_score": 0.85,
                "fact_quality": "good",
                "missing_facts_count": 2
            }},
            "quality_level": "excellent|good|acceptable|poor",
            "improvement_suggestions": ["list of specific improvements"]
        }}
        
        Be objective and thorough in your evaluation. Consider the transformation requirements, target format specifications, and fact checking results.
        
        Content to Evaluate:
        {state['converted_output']}"""
    
    final_output = call_llm(prompt)
    return {**state, "final_output": final_output}
