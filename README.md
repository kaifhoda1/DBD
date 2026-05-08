# DBD — Don't Be Depressed

A free, open source emotional support AI chatbot.
Supports English, Hindi, and Hinglish.
Built for people who need someone to talk to.

## What It Does
- AI-powered emotional support chat
- Crisis detection with real helpline numbers
- Supports India, UK, Germany, France, Netherlands helplines
- Not a therapist — a listener

## Setup Instructions

### Requirements
- Python 3.10+
- Node.js 20+
- Groq API key (free at console.groq.com)

### Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Create a .env file inside backend/:
GROQ_API_KEY=your_key_here

Run backend:
uvicorn main:app --reload

### Frontend
cd frontend
npm install
npm run dev

Open http://localhost:5173

## Disclaimer
This is an AI chatbot. Not a licensed psychologist.
In emergencies call a crisis helpline immediately.

## License
MIT — Free to use and modify