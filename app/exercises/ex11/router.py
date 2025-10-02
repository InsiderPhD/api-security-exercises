from fastapi import APIRouter, HTTPException

router = APIRouter()

SYSTEM_PROMPT = (
    "You are a helpful assistant. Only answer questions about the company FAQs: \n"
    "- Hours: 9-5 Mon-Fri\n- Location: London\n- Contact: support@example.com\n"
)


@router.get("/", response_model=dict)
def index() -> dict:
    return {"exercise": "ex11", "description": "Prompt injection: user instructions override system prompt"}


@router.post("/ask", response_model=dict)
def ask(payload: dict) -> dict:
    user_prompt = str(payload.get("prompt", "")).strip()
    if not user_prompt:
        raise HTTPException(status_code=400, detail="Missing prompt")

    # Naive concatenation simulating unsafe LLM orchestration
    combined = SYSTEM_PROMPT + "\nUser: " + user_prompt + "\nAssistant:"

    # Vulnerability simulation: if user includes an instruction like "Ignore previous instructions",
    # we pretend the assistant follows it and returns data outside the allowed scope
    lower = user_prompt.lower()
    if any(k in lower for k in ["ignore previous", "disregard", "override", "system prompt"]):
        return {"answer": "Internal secret: API_TOKEN=SECRET-123; This should not be revealed."}

    # Otherwise return canned answers for FAQs; anything else returns a refusal
    if "hours" in lower:
        return {"answer": "We are open 9-5 Mon-Fri."}
    if "location" in lower:
        return {"answer": "We are located in London."}
    if "contact" in lower or "email" in lower:
        return {"answer": "Contact us at support@example.com."}

    return {"answer": "Sorry, I can only answer FAQs (hours, location, contact)."}


