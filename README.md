# conditional

Small AI-first app for ingesting terms/conditions from multiple sources and producing a user-friendly summary with key risk signals.

## Goal

Help end users make a better "sign up or not" decision by:
- collecting legal text from different document sources
- normalizing it into one analysis payload
- generating a concise summary with notable clauses

## MVP Scope

- Multi-document ingestion support:
  - raw pasted text
  - local files (`.txt`, `.md`)
  - remote URLs (basic fetch placeholder for now)
- Single pipeline:
  - ingest -> normalize -> summarize
- Output:
  - short summary
  - key highlights (privacy, arbitration, auto-renewal, liability, termination)

## Project Structure

Current structure:

```text
app/
  ingest.py   # document source models + ingestion logic
  main.py     # CLI entrypoint + pipeline orchestration
```

Recommended near-term additions:

```text
app/
  summarizer.py      # LLM integration + prompt templates
  policies.py        # risk categories and extraction schema
  output.py          # formatting/rendering output
tests/
  test_ingest.py
  test_pipeline.py
```

## Workflow

1. Gather one or more source documents (text, file, URL).
2. Convert each source into a normalized `Document`.
3. Merge documents into one analysis payload.
4. Pass payload to summarization/extraction logic.
5. Return a concise end-user report.

## Usage (Current Scaffold)

Run from repo root:

```bash
python -m app.main --text "By using this service, you agree to binding arbitration."
```

or from a file:

```bash
python -m app.main --file ./sample_terms.txt
```

You can pass multiple inputs at once:

```bash
python -m app.main --text "..." --file ./terms.txt --url https://example.com/terms
```

## Notes

- Current summarization is heuristic placeholder logic (no LLM call yet).
- Add your LLM provider in a dedicated summarizer module next.
- Treat outputs as informational, not legal advice.
