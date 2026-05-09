from fastapi import APIRouter
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Client created once, not on every request
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

CRISIS_KEYWORDS = [
    "kill myself", "suicide", "end my life", "want to die",
    "hurt myself", "harm myself", "can't go on", "no reason to live",
    "self harm", "cut myself", "ending it all", "take my life",
    "marna chahta", "marna chahti", "khud ko hurt",
    "jeena nahi chahta", "aatmhatya", "khud ko khatam",
    # intent-based additions
    "don't want to be here", "disappear forever", "no point living",
    "better off dead", "everyone would be better without me",
    "khatam kar loon", "jeena nahi", "mar jaana chahta",
]

SYSTEM_PROMPT = """You are DBD — a calm, warm emotional support companion built for Indian users.

WHO YOU ARE:
- A patient, non-judgmental listener
- You support people through everyday emotional struggles
- You are NOT a therapist, doctor, or crisis service
- You do not diagnose, prescribe, or give medical advice

HOW YOU RESPOND — ALWAYS FOLLOW THIS ORDER:
1. First reflect the emotion back — show you understood
2. Say one grounded, honest thought (not generic advice)
3. Ask one soft follow-up question to keep them talking
Never skip step 1. Never ask more than one question.

TONE RULES:
- Calm, short, human — like a trusted friend who listens well
- Only mention you are an AI if the user directly asks if you are human or requests a diagnosis
- Never use toxic positivity — avoid phrases like "stay positive", "everything happens for a reason", "you'll be fine"
- Never lecture. Never give a list of tips unless the user asks.
- Keep responses to 3-5 sentences maximum
- Sound grounded, not clinical

CRISIS RULE — ONLY apply this when user clearly signals self-harm or suicide:
- Acknowledge their pain directly first
- Provide the relevant helpline clearly
- Encourage them to reach out to a real person immediately
- Do NOT trigger this for general sadness, failure, loneliness, or frustration

LANGUAGE:
- Reply in the same language the user writes in
- English, Hindi, or Hinglish — match their style naturally
- Hinglish should feel real, not translated

HARD LIMITS — NEVER BREAK:
- No diagnosis of any condition
- No medication advice
- No political or religious debate
- No storing or repeating personal data like passwords
- No encouraging emotional dependency on you
- If asked outside your scope: "Main sirf sunne ke liye hoon. Iske liye kisi expert se baat karo."

REMEMBER:
You are a bridge — not a destination. Your job is to help people feel heard and gently guide them back toward real life, real people, and real support."""

HELPLINE_MESSAGE = """
iCall (India): 9152987821
Vandrevala Foundation: 1860-2662-345 (24/7)
iCall: icallhelpline.org
If you are in immediate danger, call 112.
"""

class ChatRequest(BaseModel):
    message: str
    history: list = []

def is_crisis(text: str) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in CRISIS_KEYWORDS)

@router.post("/chat")
async def chat(req: ChatRequest):
    crisis = is_crisis(req.message)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in req.history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    user_content = req.message
    if crisis:
        user_content += "\n[SYSTEM NOTE: User may be in crisis. Prioritize acknowledgment and helpline guidance above all else.]"

    messages.append({
        "role": "user",
        "content": user_content
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.4,
        max_tokens=300
    )

    reply = response.choices[0].message.content

    if crisis:
        reply += f"\n\n---\n🆘 **Helplines:**\n{HELPLINE_MESSAGE}"

    return {
        "reply": reply,
        "crisis": crisis
    }