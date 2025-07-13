import logging
from typing import Dict, Any, Optional
from Agent_Invoker import create_transformation_graph, ContentState

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_user_input() -> str | None:
    """Get content input from user with validation."""
    print("\n=== Content Transformation System ===")
    print("Enter your content to transform (or 'quit' to exit):")
    print("(Type 'DONE' on a new line when finished)")
    print("Examples: emails, reports, articles, technical documents, etc.")
    
    lines = []
    
    while True:
        try:
            line = input()
            
            if line.lower() == 'quit':
                return None
            
            if line.strip().upper() == 'DONE':
                break
            
            lines.append(line)
                
        except EOFError:
            break
    
    content = '\n'.join(lines)
    if not content.strip():
        print("No content provided. Please enter some content.")
        return get_user_input()
    
    return content

def display_results(result: Dict[str, Any]):
    """Display transformation results in a formatted way."""
    print("\n" + "="*50)
    print("TRANSFORMATION RESULTS")
    print("="*50)
    
    # Show what the input preprocessor detected
    if "user_preferences" in result:
        prefs = result["user_preferences"]
        print("\n🔍 INPUT ANALYSIS:")
        print("-" * 30)
        print(f"Detected Format: {prefs.get('current_format', 'unknown')}")
        print(f"Target Format: {prefs.get('target_format', 'auto')}")
        print(f"Target Complexity: {prefs.get('complexity', 'auto')}")
        print(f"Target Tone: {prefs.get('tone', 'auto')}")
        print(f"Transformation Reason: {prefs.get('transformation_reason', 'Improve readability')}")
    
    print("\n📊 STYLE ANALYSIS:")
    print("-" * 30)
    print(result.get("analysis", "No analysis available"))
    
    print("\n📋 TRANSFORMATION PLAN:")
    print("-" * 30)
    print(result.get("transformation_plan", "No plan available"))
    
    print("\n🔄 CONVERTED OUTPUT:")
    print("-" * 30)
    print(result.get("converted_output", "No output available"))
    
    print("\n✅ QUALITY ASSESSMENT:")
    print("-" * 30)
    print(result.get("final_output", "No quality assessment available"))
    
    print("\n" + "="*50)

def process_transformation_with_feedback(graph, raw_input: str, user_suggestions: Optional[str] = None) -> Dict[str, Any]:
    """Process transformation with optional user suggestions for improvement."""
    
    # Create initial state with raw_input for the preprocessor
    state: ContentState = {
        "raw_input": raw_input,
        "input_content": "",
        "user_preferences": {},
        "user_suggestions": user_suggestions,
        "analysis": "",
        "transformation_plan": "",
        "converted_output": "",
        "final_output": ""
    }
    
    print("\n🔄 Processing transformation...")
    logger.info("Starting content transformation workflow with input preprocessor")
    
    result = graph.invoke(state)
    
    return result

def main():
    """Main application loop with error handling and user feedback."""
    graph = create_transformation_graph()
    
    while True:
        try:
            # Get user input
            user_input = get_user_input()
            if user_input is None:
                print("Goodbye!")
                break
            
            result = process_transformation_with_feedback(graph, user_input)
            
            display_results(result)
            
            # Feedback loop
            max_attempts = 3
            attempt = 1
            
            while attempt <= max_attempts:
                print(f"\n=== Feedback (Attempt {attempt}/{max_attempts}) ===")
                print("Rate the transformation (1-5, or 'skip'):")
                rating = input().strip()
                
                if rating.lower() == 'skip':
                    break
                
                if not rating.isdigit() or not (1 <= int(rating) <= 5):
                    print("Invalid rating. Please enter a number between 1-5.")
                    continue
                
                rating_val = int(rating)
                logger.info(f"User rating: {rating_val}/5")
                
                if rating_val >= 3:
                    print(f"Thank you for your feedback ({rating_val}/5)!")
                    break
                else:
                    print(f"Rating {rating_val}/5 indicates room for improvement.")
                    
                    if attempt < max_attempts:
                        print(f"\nLet's try to improve the transformation (attempt {attempt + 1}/{max_attempts})")
                        
                        # Get user suggestions
                        print("Please provide specific suggestions for improvement:")
                        print("(e.g., 'Make it more casual', 'Simplify the language', 'Add more examples')")
                        suggestions = input().strip()
                        if not suggestions:
                            suggestions = "Please improve the overall quality and make it more engaging."
                        
                        # Re-run transformation with suggestions
                        result = process_transformation_with_feedback(graph, user_input, suggestions)
                        
                        
                        display_results(result)
                        
                        attempt += 1
                    else:
                        print("Maximum attempts reached. Thank you for your patience!")
                        break
            
            print("\nTransform another piece of content? (y/n):")
            continue_choice = input().strip().lower()
            if continue_choice not in ['y', 'yes']:
                print("Goodbye!")
                break
                
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            break
        except Exception as e:
            logger.error(f"Error during transformation: {str(e)}")
            print(f"\n❌ Error occurred: {str(e)}")
            print("Please try again.")
            continue

if __name__ == "__main__":
    main()
