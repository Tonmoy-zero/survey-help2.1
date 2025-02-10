import sys
import logging
from config import verify_api_key
from chat_handler import ChatHandler
from error_handler import handle_error

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for the survey chatbot."""
    try:
        # Verify API key
        logger.info("Verifying API key...")
        api_key = verify_api_key()

        # Initialize chat handler
        logger.info("Initializing chat handler...")
        chat_handler = ChatHandler(api_key)

        print("\n=== Survey Chatbot Initialized ===")
        print("Type your question or 'quit' to exit.")
        print("=" * 35 + "\n")

        # Main interaction loop
        while True:
            try:
                # Get user input with clear prompt
                print("\nYour question: ", end='', flush=True)
                user_input = input()

                # Log received input (excluding sensitive data)
                logger.info("Received user input of length: %d", len(user_input))

                # Check for quit command
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\nThank you for using the Survey Chatbot. Goodbye!")
                    break

                # Handle empty input
                if not user_input.strip():
                    print("Please type a question or 'quit' to exit.")
                    continue

                # Process question and get response
                logger.info("Processing question...")
                response = chat_handler.process_question(user_input)

                # Print response with clear formatting
                print("\nChatbot:", response)

            except EOFError:
                logger.error("EOF Error encountered during input")
                print("\nError reading input. Please try again.")
                continue

            except KeyboardInterrupt:
                print("\nExiting...")
                break

            except Exception as e:
                error_msg = handle_error(e, "processing your request")
                print(f"\nError: {error_msg}")
                logger.exception("Error during question processing")

    except Exception as e:
        error_msg = handle_error(e, "initializing the chatbot")
        print(f"\nFatal Error: {error_msg}")
        logger.exception("Fatal error during initialization")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical("Unhandled exception in main", exc_info=True)
        sys.exit(1)