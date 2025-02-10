import os
from typing import Dict, Any

# Model configuration
GENERATION_CONFIG: Dict[str, Any] = {
    "temperature": 0.5,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

MODEL_NAME = "gemini-1.5-flash"

# Environment checks
def verify_api_key() -> str:
    """Verify and return the Gemini API key."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY environment variable is not set")
    return api_key

# Survey categories for validation
SURVEY_CATEGORIES = {
    "demographics": ["race", "ethnicity", "housing situation"],
    "finance": ["income", "investable assets", "credit score"],
    "entertainment": ["television", "streaming", "movies", "video games"],
    "health": ["medical conditions", "diabetes", "COPD"],
    "employment": ["job title", "company", "industry"]
}
