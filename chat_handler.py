from typing import Optional, Dict, Any
import google.generativeai as genai
from config import GENERATION_CONFIG, MODEL_NAME
from data_validator import DataValidator
from error_handler import handle_error, APIError

class ChatHandler:
    """Handles chat interactions with the Gemini AI model."""

    def __init__(self, api_key: str):
        """
        Initialize the chat handler.

        Args:
            api_key: Gemini AI API key
        """
        self.validator = DataValidator()
        self.setup_model(api_key)

    def setup_model(self, api_key: str) -> None:
        """
        Configure and initialize the Gemini AI model.

        Args:
            api_key: Gemini AI API key
        """
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(
                model_name=MODEL_NAME,
                generation_config=GENERATION_CONFIG
            )
            self.chat_session = self.initialize_chat()
        except Exception as e:
            raise APIError(f"Failed to initialize Gemini AI model: {str(e)}")

    def initialize_chat(self) -> Any:
        """
        Initialize a new chat session with context.

        Returns:
            Initialized chat session
        """
        survey_context = """You are 1mDC, a survey-focused chatbot. Based on the survey data:
        - Household yearly income: $100,000 to $200,000
        - Annual income before tax: Range from $150,000 to $200,000
        - Company types: Manufacturing, IT, Construction, Transportation
        - Job sectors: IT, Information technology, Human resource
        - Housing: Homeowner
        - Entertainment: Netflix, Hulu, Amazon Prime, Apple TV+, Disney+
        - Health conditions: Type 2 diabetes, COPD, migraine
        - Credit score: 600 to 799

        Provide concise, accurate responses based on this data."""

        return self.model.start_chat(history=[
            {
                "role": "user",
                "parts": [survey_context]
            }
        ])

    def process_question(self, question: str) -> str:
        """
        Process a user question and return an appropriate response.

        Args:
            question: The user's question

        Returns:
            The chatbot's response
        """
        try:
            # Sanitize and validate input
            cleaned_question = self.validator.sanitize_input(question)
            if not self.validator.validate_question(cleaned_question):
                return "I'm sorry, but I couldn't understand your question. Could you please rephrase it?"

            # Get response from model with specific context reminder
            context_reminder = "Remember to answer based on the survey data provided. Be direct and specific in your response."
            full_question = f"{context_reminder} Question: {cleaned_question}"

            # For household income questions, provide a direct response
            if any(term in cleaned_question.lower() for term in ['household income', 'household yearly income']):
                return "Based on the survey data, the household yearly income is between $100,000 to $200,000."

            response = self.chat_session.send_message(full_question)

            if not response.text:
                return "I apologize, but I couldn't generate a response. Please try asking your question differently."

            return response.text.strip()

        except Exception as e:
            return handle_error(e, "processing your question")