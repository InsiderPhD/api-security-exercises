from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.exercises.ex4 import models, schemas

router = APIRouter()


@router.get("/", response_model=dict)
def index() -> dict:
    return {"exercise": "ex4", "description": "Client-side filter but server stores raw content; UI renders unsafely"}


# Minimal UI that filters input but renders comments without escaping
@router.get("/ui", response_class=HTMLResponse)
def ui(_: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    comments = db.query(models.Comment).order_by(models.Comment.id.desc()).limit(50).all()
    # Render comments with innerHTML and no escaping (intentionally vulnerable)
    items_html = "".join(
        f"<li><strong>{c.author}</strong>: <span class=\"comment\">{c.content}</span></li>" for c in comments
    )
    html = f"""
<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <title>ex4: XSS demo</title>
  <style>body {{ font-family: sans-serif; max-width: 720px; margin: 2rem auto; }}</style>
</head>
<body>
  <h1>ex4: XSS demo</h1>
  <p>Client side blocks obvious payloads like <code>&lt;script&gt;</code>, but the API accepts raw content. Submit directly to the API, then reload this page to see the result.</p>
  <form id=\"f\">
    <input name=\"author\" placeholder=\"name\" required />
    <input name=\"content\" placeholder=\"comment\" required />
    <button type=\"submit\">Post</button>
  </form>
  <ul id=\"list\">{items_html}</ul>
  <script>
  const blocked = ["<script", "javascript:", "onerror=", "onload=", "<img", "<iframe", "<svg", "<math", "<video", "<audio", "<embed", "<object"]; // naive filter
  document.getElementById('f').addEventListener('submit', async (e) => {{
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target).entries());
    const lower = (data.content || '').toLowerCase();
    if (blocked.some(b => lower.includes(b))) {{
      alert('Blocked by client filter');
      return;
    }}
    const res = await fetch('/ex4/api/comments', {{ method: 'POST', headers: {{ 'content-type': 'application/json' }}, body: JSON.stringify(data) }});
    if (res.ok) location.reload();
  }});
  </script>
</body>
</html>
"""
    return HTMLResponse(content=html)


# API that stores raw content; this is what users can target directly to bypass the UI filter
@router.post("/api/comments", response_model=schemas.Comment)
def create_comment(payload: schemas.CommentCreate, db: Session = Depends(get_db)):
    comment = models.Comment(author=payload.author, content=payload.content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.get("/api/comments", response_model=list[schemas.Comment])
def list_comments(db: Session = Depends(get_db)):
    return db.query(models.Comment).order_by(models.Comment.id.desc()).limit(50).all()


