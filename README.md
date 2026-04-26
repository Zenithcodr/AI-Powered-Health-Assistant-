# AI-Powered Medical Chatbot (Mistral)

A Streamlit-based medical guidance chatbot that uses the Mistral API with backend-only secret handling.

## What This Project Does

This chatbot is focused on health-related guidance only.

- Accepts medical and wellness questions
- Refuses non-medical questions politely
- Detects emergency-risk phrases and escalates immediately
- Uses Mistral API when key is configured
- Falls back to local basic guidance if API is unavailable

## Important Disclaimer

This application is for informational purposes only.
It does not provide medical diagnosis, treatment, or emergency care.
Always consult a licensed healthcare professional for medical decisions.
If this is an emergency, contact your local emergency number immediately.

## Key Features

- Medical-only query gate
- Emergency signal detection
- Mistral-only provider flow
- API key kept in backend (not in frontend UI)
- Chat-style interface with conversation history
- Clear chat option

## Tech Stack

- Python 3.13+
- Streamlit
- OpenAI Python SDK (used as Mistral-compatible client via base URL)
- python-dotenv

## Project Structure

- app.py: Main Streamlit application and chatbot logic
- requirements.txt: Python dependencies
- .env.example: Backend environment template
- .gitignore: Prevents secrets and caches from being committed

## Local Setup

1. Clone the repository:

   git clone https://github.com/Zenithcodr/AI-Powered-Health-Assistant-.git
   cd AI-Powered-Health-Assistant-

2. Install dependencies:

   python -m pip install -r requirements.txt

3. Create a .env file in the project root:

   MISTRAL_API_KEY=your_mistral_api_key
   MISTRAL_MODEL=mistral-small-latest

4. Run the app:

   python -m streamlit run app.py

5. Open in browser:

   http://localhost:8501

## Streamlit Cloud Deployment

1. Push code to GitHub.
2. Create a new Streamlit Community Cloud app and point it to this repository.
3. Set Secrets in Streamlit Cloud:

   MISTRAL_API_KEY = your_mistral_api_key
   MISTRAL_MODEL = mistral-small-latest

4. Deploy with app.py as the entrypoint.

## Security Notes

- Never commit real API keys.
- Keep .env local only.
- Rotate API keys if they were ever shared publicly.

## Changelog (Current Upgrade)

- Removed old GPT-2 and multi-provider flow
- Migrated to Mistral-only backend architecture
- Added backend-only key handling
- Added strict medical-domain filtering
- Added emergency escalation behavior
- Replaced old readme with this complete README

## License

Use this project for learning and portfolio purposes.
Add a formal license file if you plan public reuse or contributions.
