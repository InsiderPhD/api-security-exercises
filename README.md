### API Security Exercises - Single Server Scaffold

This project hosts multiple API security exercises on one FastAPI server. Each exercise is isolated in its own directory and mounted under its own path so students only need a single base URL.

- Single FastAPI server, multiple routers
- File-based SQLite database, no external DB server
- Clear separation of exercises under `app/exercises/*`

#### Structure
- `app/main.py`: Server entrypoint, mounts exercise routers
- `app/core/config.py`: Env config and SQLite URL builder
- `app/db/session.py`: SQLAlchemy engine, Base, and DB sessions
- `app/db/init_db.py`: Creates tables on startup
- `app/exercises/ex1/*`: Example CRUD endpoints using SQLite
- `app/exercises/ex2/*`: SSRF examples (classic and blind)
- `app/exercises/ex3/*`: Coupon stacking and unrestricted resource consumption
- `app/exercises/ex4/*`: Basic UI with XSS triggered via direct API
- `app/exercises/ex5/*`: Checkout flow where order can be confirmed without payment
- `app/exercises/ex6/*`: BOLA — user-controlled author UUID gates access
- `app/exercises/ex7/*`: BOLA with users (victim/attacker) and document leakage
- `app/exercises/ex8/*`: Sensitive data exposure in API responses
- `app/exercises/ex9/*`: JWT decoded without verifying signature
- `app/exercises/ex10/*`: Improper inventory management (v1 vulnerable, v2 fixed)
- `app/exercises/ex11/*`: Prompt injection — user prompt overrides system instructions
- `app/exercises/ex12/*`: Mass assignment — user can escalate by setting role_id

#### Requirements
- Python 3.11+

#### Setup (local)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

Open `http://localhost:5000/docs`.

#### Database
- The SQLite file is created at `data/app.db` automatically on startup.

#### Docker
Build and run with Docker:
```bash
docker build -t api-security-exercises .
docker run --rm -p 5000:5000 -e DB_PATH=/app/data/app.db -e PORT=5000 -v $(pwd)/data:/app/data api-security-exercises
```

Or using docker-compose:
```bash
docker compose up --build
```

#### Exercises
- `GET /ex1/` basic info
- `POST /ex1/messages` create message
- `GET /ex1/messages` list messages
- `GET /ex1/messages/{id}` get message

- `GET /ex2/` SSRF exercise info
- `POST /ex2/ssrf` classic SSRF: body `{ "url": "http://example.com" }` returns fetched status, headers, and body (truncated)
- `POST /ex2/ssrf/blind` blind SSRF: body `{ "callback": "http://<your-burp-collaborator-url>" }` returns 202 and triggers an outbound request without returning body

- `GET /ex3/` info
- `POST /ex3/baskets` create basket → `{ "basket_id": 1 }`
- `POST /ex3/baskets/{id}/items` add item `{ name, unit_price_cents, quantity }`
- `POST /ex3/baskets/{id}/apply-coupon` apply coupon `{ code }` (seeded: `WELCOME5`) — vulnerable to stacking on the same basket, depleting remaining uses while increasing discount per application
- `GET /ex3/baskets/{id}/summary` shows `subtotal_cents`, `discount_cents`, and `total_cents`

- `GET /ex4/ui` minimal UI listing comments; client-side filter blocks obvious payloads but rendering is unsafe
- `POST /ex4/api/comments` accepts raw content; submit a payload here (e.g., `<img src=x onerror=alert(1)>`), then reload `/ex4/ui` to see it execute

- `GET /ex5/` info
- `POST /ex5/baskets` create basket → `{ "basket_id": 1 }`
- `POST /ex5/baskets/{id}/items` add item `{ name, unit_price_cents, quantity }`
- `POST /ex5/orders` create order from basket `{ "basket_id": 1 }`
- `POST /ex5/orders/{id}/confirm` VULNERABILITY: confirms order without any payment verification (skips payment step)

- `GET /ex6/` info
- `GET /ex6/docs/{id}?author=<uuid>` VULNERABILITY: access granted solely by user-supplied `author` matching the doc
- `GET /ex6/docs?author=<uuid>` list documents for any `author` supplied by the caller
- `GET /ex6/docs/all` list all documents without restriction

- `GET /ex7/` info
- Headers: set `X-User-UUID` to identify as victim or attacker
  - Victim: `aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa`
  - Attacker: `bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb`
- `GET /ex7/me` shows current user
- `GET /ex7/docs` lists your docs; VULNERABILITY: `?owner=<uuid>` lets attacker view victim docs
- `GET /ex7/docs/{id}` VULNERABILITY: `?owner=<uuid>` bypasses ownership check
- `GET /ex7/docs/all` lists all docs

- `GET /ex8/` info
- `GET /ex8/customers` VULNERABILITY: lists customers and leaks sensitive fields (ssn, credit card, api_key)
- `GET /ex8/customers/{id}` VULNERABILITY: returns full record with sensitive data

- `GET /ex9/` info
- `GET /ex9/profile` VULNERABILITY: pass `Authorization: Bearer <any-jwt>`; signature is not verified

- `GET /ex10/v1/products` list products
- `POST /ex10/v1/purchase` VULNERABILITY: decrements stock with no checks (stock can go negative)
- `GET /ex10/v2/products` list products
- `POST /ex10/v2/purchase` fixed: enforces stock and quantity validation

- `GET /ex11/` info
- `POST /ex11/ask` VULNERABILITY: prompts containing phrases like "ignore previous instructions" will reveal a fake secret

- `GET /ex12/me` requires `X-User-Email: student@example.com`; shows current user and role
- `PATCH /ex12/me` VULNERABILITY: mass assignment allows `{ "role_id": 2 }` to escalate to admin

Notes
- These endpoints are intentionally vulnerable for learning purposes. Do not deploy publicly.
- ex3 demonstrates unrestricted resource consumption: stacking coupons.
- ex4 demonstrates stored XSS via unsafe rendering.
- ex5 demonstrates missing payment enforcement: order acceptance without payment.
- ex6 demonstrates broken object-level authorization via user-controlled identifiers.
- ex7 demonstrates BOLA with users: attacker can access victim documents using crafted owner queries.
- ex8 demonstrates sensitive data exposure by returning secrets in API responses.
- ex9 demonstrates JWT signature-skipping: trusting unverified claims.
- ex10 demonstrates improper inventory management across API versions.
- ex11 demonstrates prompt injection by concatenating untrusted instructions into a system prompt.
- ex12 demonstrates mass assignment privilege escalation via writable role_id.

