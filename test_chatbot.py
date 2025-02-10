import os
import unittest
from chat_handler import ChatHandler
from data_validator import DataValidator
from config import verify_api_key

class TestChatbot(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            self.skipTest("GEMINI_API_KEY not set in environment")
        self.chat_handler = ChatHandler(self.api_key)
        self.validator = DataValidator()

    def test_api_key_verification(self):
        """Test API key verification"""
        self.assertIsNotNone(verify_api_key())

    def test_input_validation(self):
        """Test input validation"""
        # Test valid input
        self.assertTrue(self.validator.validate_question("What is the household income?"))
        # Test input sanitization
        self.assertEqual(
            self.validator.sanitize_input("What is the income?  "),
            "What is the income?"
        )

    def test_question_categorization(self):
        """Test question categorization"""
        # Test demographic question
        self.assertEqual(
            self.validator.categorize_question("What is the race distribution?"),
            "demographics"
        )
        # Test financial question
        self.assertEqual(
            self.validator.categorize_question("What is the income level?"),
            "financial"
        )

if __name__ == '__main__':
    unittest.main()
