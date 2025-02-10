git clone <your-repository-url>
   cd <repository-name>
   ```

2. **Set Up GitHub Secrets**
   - Go to your GitHub repository settings
   - Navigate to "Secrets and variables" > "Actions"
   - Add a new repository secret named "GEMINI_API_KEY" with your API key

3. **Install Dependencies Locally**
   ```bash
   pip install google-generativeai flask-login flask-wtf oauthlib twilio
   ```

4. **Set Up Environment Variables Locally**
   ```bash
   # For Linux/Mac
   export GEMINI_API_KEY=your_api_key_here
   # For Windows
   set GEMINI_API_KEY=your_api_key_here
   ```

5. **Run the Application**
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