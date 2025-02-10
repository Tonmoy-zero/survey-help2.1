# Clone the repository
   git clone <your-repository-url>
   cd <repository-name>

   # Install dependencies
   pip install google-generativeai flask-login flask-wtf oauthlib twilio

   # Set up environment variable locally
   export GEMINI_API_KEY=your_api_key_here  # Linux/Mac
   # or
   set GEMINI_API_KEY=your_api_key_here     # Windows
   ```

4. **Running the Application**
   ```bash
   python main.py
   ```

## Features

The chatbot can answer questions about:
- Company types and job information
- Financial information (income, revenue, assets)
- Demographics (race, housing, pets)
- Entertainment preferences (TV, movies, gaming)
- Education and health conditions

## Example Questions

- "What is the household income?"
- "What are the different company types?"
- "What streaming services are used?"
- "What health conditions are reported?"

## Project Structure

```
├── main.py              # Main entry point
├── chat_handler.py      # Core chatbot logic
├── config.py           # Configuration settings
├── data_validator.py   # Input validation
└── error_handler.py    # Error handling