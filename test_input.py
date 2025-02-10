import sys
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def main():
    """Test basic input/output functionality."""
    try:
        print("\n=== Input Test ===")
        print("Type something and press Enter (type 'quit' to exit):")
        print("(If you don't see your input, press Enter again)")
        sys.stdout.flush()

        while True:
            try:
                # Ensure prompt is visible
                print("\nEnter text: ", end='', flush=True)
                sys.stdout.flush()

                # Log before input attempt
                logger.info("Attempting to read input...")

                # Read input with explicit flush
                user_input = input().strip()

                # Log after input received
                logger.info(f"Received input: '{user_input}'")

                if user_input.lower() == 'quit':
                    print("Exiting...")
                    break

                # Echo input back with flush
                print(f"You typed: {user_input}", flush=True)

            except EOFError:
                logger.warning("EOFError encountered")
                print("\nEOF detected. Please try again.", flush=True)
                continue
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received")
                print("\nExiting due to interrupt...", flush=True)
                break
            except Exception as e:
                logger.error(f"Input error: {str(e)}")
                print(f"Error reading input: {str(e)}", flush=True)
                print("Please try again.", flush=True)
                continue

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()