# TraceDelta — evidence-first material document change review

**Independent AI Developer portfolio project. Not affiliated with SPEC Toolbox. Synthetic demo only. Not a structural engineering or standards-compliance tool.**

This is a **runnable MVP starter**, not the full four-week production blueprint. A FastAPI backend extracts candidate material facts from digital PDFs (local deterministic/mock or optional real Gemini), verifies exact quotes, normalizes supported numeric units, compares revisions, stores immutable document uploads, and flags explicitly linked decisions after human confirmation. A Next.js UI presents document evidence and review controls. All uploaded PDFs are stored in the database because Render's free disk is ephemeral. **Never upload confidential or real project files to a public demo.**

## What is implemented

- Next.js frontend; FastAPI REST service; PostgreSQL locally via Docker or optional SQLite; synthetic PDF fixture generator.
- Upload, PDF text parsing, immutable PDF snapshots (UUID + SHA-256), eight candidate fact types, exact quote validation, deterministic diff, explicit decision-to-property linkage, review/audit events, JSON and printable HTML exports.
- Strict `unresolved` when a field is missing, duplicated, or a numeric unit is unsupported; never misreports extraction failure as `no_change`.
- Two extractor modes: `mock` regex (offline demo/CI) and `gemini` real API (requires your key and access to configured model).
- Four Python unit tests and GitHub Actions config.

## Explicitly not yet implemented / tested

- Durable worker queue, retries/restart recovery, Alembic migrations, provider failover, OCR, complex tables, per-user auth, advanced qualifier-aware matching, schema-repair attempts, per-request spending ledger, vector RAG, automatic confidence calibration, 20-pair labeled evaluation suite and Playwright E2E tests.
- Current decision links are by *property*, not product + fully-qualified fact, so use only one synthetic product per workspace. A confirmed change flags every decision linked to that property.
- Human confirmation UI confirms changes but does **not** provide editing/re-extracting facts. Quote matching verifies text presence only, not semantics.
- Gemini endpoint is implemented but **was not live-tested with your API key**. The model ID may be unavailable to new accounts; set `GEMINI_MODEL` to a compatible model your account supports.
- Current request processing is synchronous to work on free hosting; production-grade jobs should be a second development stage.

## Run for free locally (recommended first)

### Option A: Docker

Install Docker Desktop / Docker Engine, clone or unzip the repository and run from project root:

```bash
python fixtures/create_pdfs.py # requires reportlab, or simply use PDFs already included
# If using included PDFs, skip the generation command.
docker compose up --build
```

Then visit http://localhost:3000 ; API documentation is at http://localhost:8000/docs . If Docker Compose isn't available on your machine, use Option B.

### Option B: without Docker

Python 3.12 and Node.js 22 are recommended. From the repository root:

```bash
cd services/api
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env # Windows: copy .env.example .env
# Environment is NOT automatically loaded; set env vars through your shell if needed.
uvicorn app.main:app --reload --port 8000
```

In another terminal:

```bash
cd apps/web
npm install
cp .env.example .env.local # Windows: copy .env.example .env.local
npm run dev
```

Defaults are SQLite on backend and http://localhost:8000 for frontend. For local integration use supplied synthetic fixtures `fixtures/tracedelta-v1-synthetic.pdf` and `fixtures/tracedelta-v2-synthetic.pdf`.

1. Upload V1 and V2 separately.
2. Create a decision linked to `usage_conditions`, e.g. "Recheck SC2 application".
3. Compare V1 (baseline) against V2 (revision), first using `mock` mode. `thickness` is equivalent (12 mm = 1.2 cm); `usage_conditions` and `revision_date` change.
4. Inspect quotes and open PDFs. Confirm `usage_conditions`. The decision is now `needs_review`.
5. Export JSON or print the HTML report.

## Real AI (optional)

Create a Gemini API key in Google AI Studio, check your account's supported models and free-tier data terms, then supply secrets **only to the backend**:

```bash
# Linux/macOS shell, before starting backend
export GEMINI_API_KEY='YOUR_SECRET'
export GEMINI_MODEL='YOUR_AVAILABLE_COMPATIBLE_MODEL'
```

Docker: create a root `.env` file (gitignored) with `GEMINI_API_KEY=...` and `GEMINI_MODEL=...` before `docker compose up --build`. Choose `gemini` in the UI. No key is needed for mock mode.

## Free cloud deployment: GitHub + Supabase + Render + Vercel

**Always verify current terms and quotas. Free hosting has sleeping instances and resource limits; no uptime guarantee.** The stack needs three accounts besides GitHub:

### 1. GitHub

Create a repository called `tracedelta`. **Extract this ZIP first**, then upload *all files and folders inside `tracedelta/`* using GitHub **Add file → Upload files**, keeping `apps`, `services`, `.github`, `fixtures`, and root configuration. GitHub browser upload sometimes makes nested directories cumbersome; Git CLI (`git init`, `git add .`, `git commit`, `git push`) is more reliable. Never commit `.env`, tokens, or credentials.

### 2. Supabase (PostgreSQL)

Create a Free project. From **Connect**, obtain the Postgres connection string suitable for Render (check IPv4 vs session pooler compatibility). Replace password placeholder. Set the `DATABASE_URL` environment variable on Render (do not commit it). If required, append `?sslmode=require` to the PostgreSQL URL. Database tables are currently created by SQLAlchemy at API startup; Alembic is an explicit follow-up.

Supabase free projects can pause after one week of inactivity. Free plan does not include automatic backups; export critical data manually. PDF BLOBs count against database capacity. **This is meant for tiny synthetic PDFs only**.

### 3. Render (FastAPI API)

Create a **Free Web Service** connected to the same repo:

- Runtime: Docker
- Root directory: `services/api`
- Dockerfile: `Dockerfile`
- Environment:
  - `APP_ENV=production`
  - `DATABASE_URL=<Supabase connection string>`
  - `CORS_ORIGINS=https://YOUR-VERCEL-APP.vercel.app`
  - `WRITE_TOKEN=<generate a long random secret>` (required in production; enter it manually in the frontend UI when using private editing)
  - `READ_ONLY=false` for private demo; `true` for public read-only deployment
  - `GEMINI_API_KEY=<your key>` only if enabling real AI
  - `GEMINI_MODEL=<available model>` only if enabling real AI

Render sets `PORT` automatically; Docker CMD uses it. Deploy and verify `https://YOUR-RENDER-APP.onrender.com/health`.

**Security limitation:** This MVP has a shared write token, not user accounts. Read endpoints and PDFs are public to anyone who knows/discovers the API. For public viewing, use synthetic fixtures only and `READ_ONLY=true` after loading demo data; no confidential PDFs.

### 4. Vercel (Next.js frontend)

Import the same GitHub repository. Set **Root Directory** to `apps/web` (Next.js autodetected). Add a **build-time** environment variable:

`NEXT_PUBLIC_API_URL=https://YOUR-RENDER-APP.onrender.com`

Deploy, then change Render `CORS_ORIGINS` to the exact Vercel URL and redeploy Render. If the public demo is read-only, create initial data before switching `READ_ONLY=true`, and redeploy.

Important: Render Free sleeps after inactivity and may take around a minute to wake; this can make the first request slow or the first long AI request fail. Browser refresh may be necessary. Long synchronous inference may exceed free-host limits.

## Testing

```bash
cd services/api
python -m pytest -q
```

CI also runs `npm run build` in the frontend. Mock tests **do not demonstrate real model quality**; record real evaluation separately before claiming accuracy. No field-accuracy, precision, recall or p95 performance metric is claimed here.

## Security and engineering limitations

- Do not use with proprietary engineering documents or personal data; public PDF read routes are unauthenticated.
- Never put Gemini keys or owner token into `NEXT_PUBLIC_...` variables. The write token is entered at runtime, not bundled.
- The backend rejects PDFs with no text layer and documents over 10 pages/10 MB. It validates quotes by whitespace-normalized exact substring, which does not validate model interpretation.
- A signed-in multiuser app needs real identity, tenant isolation, row-level access controls, rate limiting and stricter document permissions.
- No persistent job runner or budget enforcement yet; avoid enabling Gemini mode on an untrusted public write-enabled instance.

## Development priorities after this starter

1. Qualified fact identity and corrections/review of both extraction stages, with separate raw and human-reviewed records.
2. DB-backed persistent jobs, retry/idempotency, migrations and model spend caps.
3. A manually labeled held-out evaluation set (20 synthetic document pairs, 200 facts), baseline text diff and actual metric reports.
4. Owner authentication, storage isolation, rate limiting and richer UI evidence viewer.

See `docs/ARCHITECTURE.md` for pipeline and tradeoffs.
