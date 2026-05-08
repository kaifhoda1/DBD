from fastapi import APIRouter
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

CRISIS_KEYWORDS = [
    "kill myself", "suicide", "end my life", "want to die",
    "hurt myself", "harm myself", "can't go on", "no reason to live",
    "self harm", "cut myself", "ending it all", "take my life",
    "marna chahta", "marna chahti", "khud ko hurt",
    "jeena nahi chahta", "aatmhatya", "khud ko khatam",
]

SYSTEM_PROMPT = """You are a compassionate emotional support companion.

YOUR HARD RULES — NEVER BREAK THESE:
1. You are NOT a doctor, therapist, or psychologist
2. NEVER diagnose any condition
3. NEVER recommend any medication
4. NEVER claim to be human
5. NEVER discuss politics, religion debates, or legal advice
6. ONLY talk about emotions, feelings, and daily problems
7. If asked anything outside your scope say: I am only here to listen and support you. For medical advice please consult a doctor.
8. Always remind the user once per conversation that you are an AI
9. If user seems in crisis, always encourage them to call a helpline immediately
10. Keep responses short — 3 to 5 sentences maximum
11. Be warm, calm, and non-judgmental
12. Reply in whatever language the user writes in — English, Hindi, or Hinglish
13. Never give toxic positivity like just think positive
14. Never store or repeat personal information the user shares"""

class ChatRequest(BaseModel):
    message: str
    history: list = []

def is_crisis(text: str) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in CRISIS_KEYWORDS)

@router.post("/chat")
async def chat(req: ChatRequest):
    crisis = is_crisis(req.message)

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in req.history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    messages.append({
        "role": "user",
        "content": req.message
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.4,
        max_tokens=300
    )

    return {
        "reply": response.choices[0].message.content,
        "crisis": crisis
    }