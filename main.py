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
    while True:
        try:
            # Print prompt with explicit flush
            sys.stdout.write("\nQuestion: ")
            sys.stdout.flush()

            # Read input
            user_input = input().strip()

            # Log received input length
            logger.info(f"Received input of length: {len(user_input)}")
            return user_input

        except EOFError:
            logger.warning("EOFError encountered")
            print("\nInput error. Please try again.", flush=True)
            continue
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
            return "quit"
        except Exception as e:
            logger.error(f"Input error: {str(e)}")
            print(f"\nError reading input: {str(e)}", flush=True)
            continue

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

        # Welcome message with explicit flush
        sys.stdout.write("\n=== Survey Chatbot ===\n")
        sys.stdout.write("Ask me anything about the survey data!\n")
        sys.stdout.write("Type 'quit' to exit.\n")
        sys.stdout.write("=" * 35 + "\n")
        sys.stdout.flush()

        # Main interaction loop
        while True:
            try:
                user_input = get_user_input()

                # Check for quit command
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    sys.stdout.write("\nThank you for using the Survey Chatbot. Goodbye!\n")
                    sys.stdout.flush()
                    break

                # Handle empty input
                if not user_input:
                    sys.stdout.write("Please type a question or 'quit' to exit.\n")
                    sys.stdout.flush()
                    continue

                # Process question and get response
                logger.info("Processing question...")
                response = chat_handler.process_question(user_input)
                logger.info("Response generated successfully")

                # Print response with explicit flush
                sys.stdout.write(f"\nChatbot: {response}\n")
                sys.stdout.flush()

            except Exception as e:
                error_msg = handle_error(e, "processing your question")
                sys.stdout.write(f"\nError: {error_msg}\n")
                sys.stdout.flush()
                continue

    except Exception as e:
        error_msg = handle_error(e, "running the chatbot")
        logger.exception("Fatal error")
        sys.stdout.write(f"\nFatal Error: {error_msg}\n")
        sys.stdout.flush()
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write("\nExiting due to user interrupt...\n")
        sys.stdout.flush()
    except Exception as e:
        logger.critical("Unhandled exception in main", exc_info=True)
        sys.exit(1)