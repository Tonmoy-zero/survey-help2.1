from typing import Optional, Any
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class ChatbotError(Exception):
    """Base exception class for chatbot errors."""
    pass

class APIError(ChatbotError):
    """Exception for API-related errors."""
    pass

class ValidationError(ChatbotError):
    """Exception for data validation errors."""
    pass

def handle_error(error: Exception, context: Optional[str] = None) -> Any:
    """
    Central error handler for the chatbot.
    
    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred
    
    Returns:
        A user-friendly error message
    """
    error_msg = f"An error occurred"
    if context:
        error_msg += f" while {context}"
    
    if isinstance(error, APIError):
        logger.error(f"API Error: {str(error)}")
        return "I'm having trouble connecting to my knowledge base. Please try again in a moment."
    
    elif isinstance(error, ValidationError):
        logger.warning(f"Validation Error: {str(error)}")
        return "I couldn't understand that question. Could you please rephrase it?"
    
    else:
        logger.error(f"Unexpected Error: {str(error)}", exc_info=True)
        return "I encountered an unexpected error. Please try again or contact support."
