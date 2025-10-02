from fastapi import APIRouter, Header, HTTPException
import jwt
from jwt import InvalidTokenError

router = APIRouter()


@router.get("/", response_model=dict)
def index() -> dict:
    return {"exercise": "ex9", "description": "JWT decoded without signature verification; forge tokens easily"}


@router.get("/profile", response_model=dict)
def jwt_profile(authorization: str | None = Header(default=None)) -> dict:
    # Expecting Authorization: Bearer <token>
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    token = authorization.split(" ", 1)[1]

    try:
        # VULNERABILITY: verify_signature=False disables signature verification
        payload = jwt.decode(token, options={"verify_signature": False, "verify_aud": False})
    except InvalidTokenError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid token: {exc}")

    # Act on untrusted claims, e.g. role, email, sub
    return {
        "sub": payload.get("sub"),
        "email": payload.get("email"),
        "role": payload.get("role"),
        "claims": payload,
        "note": "Signature was NOT verified.",
    }


