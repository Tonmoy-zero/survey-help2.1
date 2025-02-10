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
            # Test the model with a simple query
            test_response = self.chat_session.send_message("Test connection")
            if test_response.text:
                logger.info("Model test response successful")
            else:
                logger.warning("Model test response was empty")
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
            survey_context = """you are 1mDC the chatbot who helps with survey. People will ask you about various questions related to survey and you will answer based on data that I give to you. You can also search the internet to come up with answer that are not included in the data.

Survey Data:
Company Types:
- Manufacturing
- Information technology
- Construction
- Transportation

Job Information:
- Job descriptions: Information technology, Human resource
- Job Titles: CTO, chief technology officer, chief information officer
- Job Responsibility: Director
- Job sector: IT

Financial Information:
- Company annual revenue: 100m - 500m
- Annual income before tax range: 150,000 - 200,000
- Household yearly income: 100,000 to 200,000
- Investable assets: more than 500,000, less than 999,999
- Credit score: 600 to 799

Demographics:
- Race/Ethnicity: White, Hispanic/Latino
- Housing: Homeowner
- Car ownership: Yes
- Pets: Cat & dog
- Voter registration: Yes
- Previous survey participation: No

Entertainment:
- TV/Streaming weekly watch time: 20 hours plus
- Video subscriptions: Netflix, Hulu, Amazon Prime, Apple TV+, Disney+
- Music streaming: YouTube Music, Spotify
- TV subscriptions: DishTV, Fios-verizon, Direct TV
- Movies in theater (12 months): 10
- Movies in theater (6 months): 4-6
- Movies in theater (2 months): 1
- Video gaming: 10-20 hours per week

Education and Health:
- Highest education: Postgraduate/Masters/MA
- Health conditions: Type 2 diabetes, COPD, migraine

If you find any question similar to this, you will respond based on the above output. If you find questions related to survey that are not included, search the internet to give the right answer.

Remember to:
1. Always provide specific answers based on the survey data
2. If the exact data isn't available, mention that and provide a relevant internet-based response
3. Keep responses concise and accurate"""

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
            logger.info(f"Processing question: {question[:50]}...")

            # Sanitize and validate input
            cleaned_question = self.validator.sanitize_input(question)
            if not self.validator.validate_question(cleaned_question):
                logger.warning("Invalid question format")
                return "I'm sorry, but I couldn't understand your question. Could you please rephrase it?"

            # Categorize the question
            category = self.validator.categorize_question(cleaned_question)
            if category:
                logger.info(f"Question categorized as: {category}")

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

            # Handle pet-related questions directly
            if any(term in lower_question for term in ['pet', 'pets', 'animal']):
                logger.info("Providing direct response for pet question")
                return "Based on the survey data, the person has both a cat and a dog."

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