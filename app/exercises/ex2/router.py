from fastapi import APIRouter, BackgroundTasks
import httpx

from app.exercises.ex2.schemas import SSRFRequest, BlindSSRFRequest, FetchedResponse

router = APIRouter()


@router.get("/", response_model=dict)
def index() -> dict:
    return {"exercise": "ex2", "description": "SSRF and blind SSRF examples"}


@router.post("/ssrf", response_model=FetchedResponse)
async def ssrf_fetch(payload: SSRFRequest) -> FetchedResponse:
    # Classic SSRF: server fetches arbitrary URL provided by user and returns content
    async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
        resp = await client.get(str(payload.url))
        # Limit body size for safety in the exercise environment
        body_text = resp.text
        if len(body_text) > 8000:
            body_text = body_text[:8000] + "... [truncated]"
        # Convert headers to str->str for schema
        headers = {k: ", ".join(v) if isinstance(v, list) else str(v) for k, v in resp.headers.items()}
        return FetchedResponse(status_code=resp.status_code, headers=headers, body=body_text)


async def _fire_and_forget(url: str) -> None:
    # Blind SSRF: make a request to the attacker-controlled URL, do not propagate result
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=5.0) as client:
            await client.get(url)
    except Exception:
        # Intentionally ignore errors to simulate blind behavior
        pass


@router.post("/ssrf/blind", status_code=202)
async def ssrf_blind(payload: BlindSSRFRequest, background_tasks: BackgroundTasks) -> dict:
    background_tasks.add_task(_fire_and_forget, str(payload.callback))
    # Return immediately without including any fetched data
    return {"status": "queued", "note": "A request will be made to the provided URL."}
