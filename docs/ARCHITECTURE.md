# TraceDelta architecture — starter scope

```text
Next.js (Vercel) ── HTTPS ── FastAPI (Render Free) ── PostgreSQL (Supabase)
                              │
                              ├── pdfplumber text layer parser
                              ├── mock extractor OR real Gemini API (server only)
                              ├── evidence validation + decimal unit normalization
                              ├── conservative deterministic diff
                              └── human review → property-linked decision status
```

The project chooses one API service and **synchronous** processing for inexpensive hosting. It is not the full worker-based target architecture; sleeping free services and synchronous API timeouts are known drawbacks. PDF binaries live in PostgreSQL for restart persistence, suitable only for very small synthetic demo files. A production system needs scoped object storage and strict access control.

## Data

- `documents`: immutable PDF binary, SHA-256, extracted per-page text.
- `comparisons`: old/new document ID, extractor version, snapshot fact candidates and comparison outcomes.
- `decisions`: user-entered title and referenced property (demo limitation: not fully qualified fact ID).
- `audit_events`: upload, comparison, decision creation and review.

`Base.metadata.create_all` initializes the starter schema. No Alembic migrations have been built. When extending the schema, add migrations before sharing a live database.

## Conservative diff

- `changed` only if both sides have exactly one evidence-validated extract for that property and normalized values are unequal.
- `unchanged` only if the two comparable normalized values are equal.
- `unresolved` if values are absent, duplicates exist, or numeric normalization fails.
- For thickness: mm/cm/m normalize to mm; for density: kg/m³ and g/cm³ normalize to kg/m³ using `Decimal`.
- No inference about structural safety, certification compliance, product applicability, or version supersession.

### Threats and known deficiencies

- Documents are untrusted prompt inputs. Gemini is told to extract but a hostile PDF can still manipulate LLM output. No model tool execution is exposed. Verify citations and review output; add adversarial tests before real documents.
- Quote checking is literal whitespace-normalized substring, not semantic verification.
- The current system does not support multiple products/conditions in one document. Multiple values for one field abstain; future work must preserve qualifiers and measurement methods.
- Public document reads mean synthetic-only public hosting. WRITE_TOKEN is a shared secret, not per-user authentication.
- Rate limits, model spend caps, long-running job orchestration, and detailed observability are follow-ups, not claimed capabilities.

## Portfolio talk track

LLM extracts candidate facts; deterministic code verifies evidence and calculates meaningful differences; people approve change interpretation; explicit dependency relationships trigger review. This deliberately separates probabilistic model behavior from auditable state transitions.
