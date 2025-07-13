from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, Any, Optional
from agents.input_preprocessor import input_preprocessor_agent
from agents.style_analysis import style_analysis_agent
from agents.transformation_plan import transformation_planning_agent
from agents.content_conversion import content_conversion_agent
from agents.quality_control import quality_control_agent

class ContentState(TypedDict):
    raw_input: str
    input_content: str
    user_preferences: Dict[str, Any]
    user_suggestions: Optional[str]
    analysis: str
    transformation_plan: str
    converted_output: str
    final_output: str

def create_transformation_graph():
    builder = StateGraph(ContentState)

    # Add the new input preprocessor as the first agent
    builder.add_node("InputPreprocessor", input_preprocessor_agent)
    builder.add_node("StyleAnalysis", style_analysis_agent)
    builder.add_node("TransformationPlanning", transformation_planning_agent)
    builder.add_node("ContentConversion", content_conversion_agent)
    builder.add_node("QualityControl", quality_control_agent)

    # Set the input preprocessor as the entry point
    builder.set_entry_point("InputPreprocessor")
    
    # Update the workflow to start from input preprocessor
    builder.add_edge("InputPreprocessor", "StyleAnalysis")
    builder.add_edge("StyleAnalysis", "TransformationPlanning")
    builder.add_edge("TransformationPlanning", "ContentConversion")
    builder.add_edge("ContentConversion", "QualityControl")
    builder.add_edge("QualityControl", END)

    return builder.compile()
