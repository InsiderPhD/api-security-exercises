from pydantic import BaseModel, HttpUrl, AnyHttpUrl


class SSRFRequest(BaseModel):
    # Intentionally accepts any http(s) URL to illustrate the vulnerability
    url: AnyHttpUrl


class BlindSSRFRequest(BaseModel):
    # In blind SSRF we still take a URL but won't return the body
    callback: AnyHttpUrl


class FetchedResponse(BaseModel):
    status_code: int
    headers: dict[str, str]
    body: str
