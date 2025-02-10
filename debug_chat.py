import sys
import logging
from config import verify_api_key
from chat_handler import ChatHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def main():
    """Debug script to test chatbot functionality."""
    try:
        logger.info("Starting debug session...")
        
        # Test API key
        logger.info("Testing API key...")
        api_key = verify_api_key()
        logger.info("API key verified successfully")
        
        # Test chat handler initialization
        logger.info("Testing chat handler initialization...")
        chat_handler = ChatHandler(api_key)
        logger.info("Chat handler initialized successfully")
        
        # Test specific question
        test_question = "What is the household income according to the survey?"
        logger.info(f"Testing specific question: {test_question}")
        
        response = chat_handler.process_question(test_question)
        logger.info(f"Response received: {response}")
        
        print("\nTest Results:")
        print("-" * 50)
        print(f"Question: {test_question}")
        print(f"Response: {response}")
        
    except Exception as e:
        logger.error(f"Debug test failed: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
