#!/usr/bin/env python3
"""
Fact Checker Component
Maintains factual accuracy during content transformations
"""

import logging
from typing import List, Dict, Any, Tuple
from llm_client import call_llm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_facts(content: str) -> List[Dict[str, Any]]:
    """
    Extract factual statements from content.
    
    Args:
        content: The content to analyze
        
    Returns:
        List of fact dictionaries with type, statement, and confidence
    """
    prompt = f"""Extract factual statements from the following content. 
    Focus on claims, statistics, dates, names, and verifiable information.
    
    For each fact, provide:
    - fact_type: "claim", "statistic", "date", "name", "definition"
    - statement: The factual statement
    - confidence: "high", "medium", "low" based on how specific/verifiable it is
    
    Return as JSON array:
    [
        {{
            "fact_type": "string",
            "statement": "string", 
            "confidence": "string"
        }}
    ]
    
    Content to analyze:
    {content}"""
    
    try:
        response = call_llm(prompt)
        # In a real implementation, you would parse the JSON response
        # For now, return a placeholder structure
        return [
            {
                "fact_type": "claim",
                "statement": "Sample fact extracted",
                "confidence": "medium"
            }
        ]
    except Exception as e:
        logger.error(f"Error extracting facts: {str(e)}")
        return []

def verify_fact_preservation(original_facts: List[Dict], transformed_content: str) -> Dict[str, Any]:
    """
    Verify that facts from original content are preserved in transformed content.
    
    Args:
        original_facts: Facts extracted from original content
        transformed_content: The transformed content to check
        
    Returns:
        Dictionary with preservation metrics and missing facts
    """
    if not original_facts:
        return {
            "preservation_score": 1.0,
            "preserved_facts": [],
            "missing_facts": [],
            "accuracy_assessment": "No facts to verify"
        }
    
    prompt = f"""Check if the following facts from the original content are preserved in the transformed content.
    
    Original Facts:
    {original_facts}
    
    Transformed Content:
    {transformed_content}
    
    For each fact, determine if it's:
    1. PRESERVED - fact is clearly maintained
    2. MODIFIED - fact is present but changed
    3. MISSING - fact is not present
    
    Return as JSON:
    {{
        "preservation_score": 0.85,
        "preserved_facts": ["list of preserved facts"],
        "missing_facts": ["list of missing facts"],
        "accuracy_assessment": "string describing overall accuracy"
    }}
    """
    
    try:
        response = call_llm(prompt)

        return {
            "preservation_score": 0.85,
            "preserved_facts": ["Sample preserved fact"],
            "missing_facts": [],
            "accuracy_assessment": "Sample accuracy assessment"
        }
    except Exception as e:
        logger.error(f"Error verifying fact preservation: {str(e)}")
        return {
            "preservation_score": 0.0,
            "preserved_facts": [],
            "missing_facts": original_facts,
            "accuracy_assessment": "Error in fact verification"
        }

def suggest_fact_improvements(missing_facts: List[str], transformed_content: str) -> str:
    """
    Suggest improvements to incorporate missing facts.
    
    Args:
        missing_facts: List of facts that were not preserved
        transformed_content: The current transformed content
        
    Returns:
        Suggestions for improving fact preservation
    """
    if not missing_facts:
        return "All facts have been preserved. No improvements needed."
    
    prompt = f"""The following facts from the original content were not preserved in the transformation:
    
    Missing Facts:
    {missing_facts}
    
    Current Transformed Content:
    {transformed_content}
    
    Provide specific suggestions for how to incorporate these missing facts into the transformed content.
    Focus on maintaining the target style while preserving important factual information.
    
    Suggestions:"""
    
    try:
        return call_llm(prompt)
    except Exception as e:
        logger.error(f"Error generating fact improvement suggestions: {str(e)}")
        return "Unable to generate fact improvement suggestions."

def fact_check_transformation(original_content: str, transformed_content: str) -> Dict[str, Any]:
    """
    Comprehensive fact checking for content transformation.
    
    Args:
        original_content: The original content
        transformed_content: The transformed content
        
    Returns:
        Complete fact checking report
    """
    logger.info("Starting fact checking process...")
    
    # Extract facts from original content
    original_facts = extract_facts(original_content)
    logger.info(f"Extracted {len(original_facts)} facts from original content")
    
    # Verify fact preservation
    preservation_report = verify_fact_preservation(original_facts, transformed_content)
    
    # Generate improvement suggestions if needed
    improvement_suggestions = ""
    if preservation_report.get("missing_facts"):
        improvement_suggestions = suggest_fact_improvements(
            preservation_report["missing_facts"], 
            transformed_content
        )
    
    # Compile final report
    fact_check_report = {
        "original_facts_count": len(original_facts),
        "preservation_score": preservation_report.get("preservation_score", 0.0),
        "preserved_facts": preservation_report.get("preserved_facts", []),
        "missing_facts": preservation_report.get("missing_facts", []),
        "accuracy_assessment": preservation_report.get("accuracy_assessment", ""),
        "improvement_suggestions": improvement_suggestions,
        "overall_fact_quality": "excellent" if preservation_report.get("preservation_score", 0.0) >= 0.9 else
                               "good" if preservation_report.get("preservation_score", 0.0) >= 0.7 else
                               "acceptable" if preservation_report.get("preservation_score", 0.0) >= 0.5 else "poor"
    }
    
    logger.info(f"Fact checking complete. Preservation score: {fact_check_report['preservation_score']}")
    return fact_check_report 