from typing import Optional, Dict, Any
import google.generativeai as genai
from config import GENERATION_CONFIG, MODEL_NAME
from data_validator import DataValidator
from error_handler import handle_error, APIError
import sys
import logging

logger = logging.getLogger(__name__)

class ChatHandler:
    """Handles chat interactions with the Gemini AI model."""

    def __init__(self, api_key: str):
        """
        Initialize the chat handler.

        Args:
            api_key: Gemini API key
        """
        self.validator = DataValidator()
        try:
            self.setup_model(api_key)
            logger.info("Chat handler initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize chat handler: {str(e)}")
            raise

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
            logger.info("Model setup completed successfully")
        except Exception as e:
            logger.error(f"Model setup failed: {str(e)}")
            raise APIError(f"Failed to initialize Gemini AI model: {str(e)}")

    def initialize_chat(self) -> Any:
        """
        Initialize a new chat session with context.

        Returns:
            Initialized chat session
        """
        try:
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

            session = self.model.start_chat(history=[
                {
                    "role": "user",
                    "parts": [survey_context]
                }
            ])
            logger.info("Chat session initialized successfully")
            return session
        except Exception as e:
            logger.error(f"Failed to initialize chat session: {str(e)}")
            raise

    def process_question(self, question: str) -> str:
        """
        Process a user question and return an appropriate response.

        Args:
            question: The user's question

        Returns:
            The chatbot's response
        """
        try:
            # Log incoming question
            logger.info(f"Processing question of length: {len(question)}")

            # Sanitize and validate input
            cleaned_question = self.validator.sanitize_input(question)
            if not self.validator.validate_question(cleaned_question):
                logger.warning("Invalid question format")
                return "I'm sorry, but I couldn't understand your question. Could you please rephrase it?"

            # Direct responses for specific questions
            lower_question = cleaned_question.lower()

            # Handle household income questions directly
            if any(term in lower_question for term in ['household income', 'household yearly income']):
                logger.info("Providing direct response for household income question")
                return "Based on the survey data, the household yearly income is between $100,000 to $200,000."

            # Handle health condition questions directly
            if any(term in lower_question for term in ['health', 'medical condition', 'disease']):
                logger.info("Providing direct response for health conditions")
                return "Based on the survey data, the reported health conditions are: Type 2 diabetes, COPD, and migraine."

            # Get response from model with specific context reminder
            context_reminder = "Remember to answer based on the survey data provided. Be direct and specific in your response."
            full_question = f"{context_reminder} Question: {cleaned_question}"

            logger.info("Sending question to model")
            response = self.chat_session.send_message(full_question)

            if not response.text:
                logger.warning("Empty response received from model")
                return "I apologize, but I couldn't generate a response. Please try asking your question differently."

            logger.info("Successfully generated response")
            return response.text.strip()

        except Exception as e:
            logger.exception("Error processing question")
            return handle_error(e, "processing your question")