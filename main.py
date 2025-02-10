import sys
import logging
from config import verify_api_key
from chat_handler import ChatHandler
from error_handler import handle_error
from flask import Flask, render_template, request, jsonify

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

app = Flask(__name__)
chat_handler = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        question = data.get('question', '')

        if not question:
            return jsonify({'response': 'Please ask a question.'}), 400

        if not chat_handler:
            return jsonify({'response': 'Chatbot is not initialized properly.'}), 500

        response = chat_handler.process_question(question)
        return jsonify({'response': response})

    except Exception as e:
        error_msg = handle_error(e, "processing your question")
        return jsonify({'response': f"Error: {error_msg}"}), 500

def main():
    """Main entry point for the survey chatbot."""
    try:
        # Verify API key
        logger.info("Verifying API key...")
        api_key = verify_api_key()

        # Initialize chat handler
        logger.info("Initializing chat handler...")
        global chat_handler
        chat_handler = ChatHandler(api_key)
        logger.info("Chat handler initialized successfully")

        # Run the Flask application
        app.run(host='0.0.0.0', port=5000)

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