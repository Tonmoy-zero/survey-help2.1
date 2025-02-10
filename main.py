import sys
import logging
from config import verify_api_key
from chat_handler import ChatHandler
from error_handler import handle_error

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('chatbot.log')
    ]
)
logger = logging.getLogger(__name__)

def get_user_input() -> str:
    """Get user input with proper error handling."""
    try:
        # Ensure prompt is visible
        print("\nYour question (type 'quit' to exit): ", end='', flush=True)
        sys.stdout.flush()

        # Log attempt to read input
        logger.info("Waiting for user input...")

        # Read input with timeout
        user_input = input().strip()

        # Log received input (excluding sensitive data)
        logger.info(f"Received input of length: {len(user_input)}")

        return user_input

    except EOFError:
        logger.warning("EOFError encountered")
        print("\nInput error detected. Please try again.", flush=True)
        return ""
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
        return "quit"
    except Exception as e:
        logger.error(f"Input error: {str(e)}")
        print(f"\nError reading input: {str(e)}", flush=True)
        return ""

def main():
    """Main entry point for the survey chatbot."""
    try:
        # Verify API key
        logger.info("Verifying API key...")
        api_key = verify_api_key()

        # Initialize chat handler
        logger.info("Initializing chat handler...")
        chat_handler = ChatHandler(api_key)
        logger.info("Chat handler initialized successfully")

        print("\n=== Survey Chatbot Initialized ===", flush=True)
        print("Type your question or 'quit' to exit.", flush=True)
        print("=" * 35 + "\n", flush=True)
        sys.stdout.flush()

        # Main interaction loop
        while True:
            user_input = get_user_input()

            # Check for quit command
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nThank you for using the Survey Chatbot. Goodbye!", flush=True)
                break

            # Handle empty input
            if not user_input:
                print("Please type a question or 'quit' to exit.", flush=True)
                continue

            # Process question and get response
            logger.info(f"Processing question of length: {len(user_input)}")
            response = chat_handler.process_question(user_input)
            logger.info("Response generated successfully")

            # Print response with flush
            print("\nChatbot:", response, flush=True)
            sys.stdout.flush()

    except Exception as e:
        error_msg = handle_error(e, "running the chatbot")
        logger.exception("Fatal error")
        print(f"\nFatal Error: {error_msg}", flush=True)
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting due to user interrupt...", flush=True)
    except Exception as e:
        logger.critical("Unhandled exception in main", exc_info=True)
        sys.exit(1)