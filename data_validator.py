from typing import Any, Dict, List, Optional
import re
from error_handler import ValidationError

class DataValidator:
    """Validates and sanitizes input data for the chatbot."""
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """
        Sanitizes user input by removing special characters and excess whitespace.
        
        Args:
            text: The input text to sanitize
            
        Returns:
            Sanitized text
        """
        # Remove special characters except basic punctuation
        text = re.sub(r'[^\w\s?.!,]', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text.strip()
    
    @staticmethod
    def validate_question(question: str) -> bool:
        """
        Validates if the input is a proper question.
        
        Args:
            question: The question to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not question:
            return False
        
        # Check minimum length
        if len(question) < 3:
            return False
            
        # Check maximum length
        if len(question) > 500:
            return False
            
        return True
    
    @staticmethod
    def categorize_question(question: str) -> Optional[str]:
        """
        Categorizes the question into a survey category.
        
        Args:
            question: The question to categorize
            
        Returns:
            Category name or None if uncategorized
        """
        question = question.lower()
        
        categories = {
            'demographics': ['age', 'gender', 'race', 'ethnicity', 'location'],
            'financial': ['income', 'salary', 'revenue', 'assets'],
            'health': ['medical', 'health', 'condition', 'disease'],
            'entertainment': ['tv', 'movie', 'game', 'streaming'],
            'employment': ['job', 'work', 'company', 'industry']
        }
        
        for category, keywords in categories.items():
            if any(keyword in question for keyword in keywords):
                return category
                
        return None
