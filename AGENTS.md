# AGENTS.md

This file provides guidance for AI coding assistants and contributors working on AI-Assisted-Cloud-Load-Tester.

## Project Goal

AI-Assisted-Cloud-Load-Tester is a cloud computing portfolio project. It ingests historical API logs, anonymizes user identifiers, generates synthetic user personas, runs persona driven load tests and reports performance bottlenecks.

Prioritize a working, well tested MVP over unnecessary complexity.

## Core Principles

- Keep the project easy to run locally.
- Prefer simple, readable Python over clever abstractions.
- Use strong typing, validation, and tests for core behavior.
- Keep components small and independently testable.
- Avoid adding managed cloud dependencies to the MVP.
- Document every command needed to reproduce results.
- Never commit secrets, credentials, raw PII, or machine-specific files.

## Preferred Stack

- Python 3.11+
- FastAPI for the demo API
- Typer for the CLI
- SQLAlchemy or SQLModel for persistence
- SQLite for local MVP storage
- httpx or aiohttp for the async load agent
- pytest for tests
- Ruff for linting and formatting
- Docker and Docker Compose for local development
- Kubernetes manifests for cloud-native deployment

## Repository Expectations

Expected structure:

```text
ai-assisted-cloud-load-tester/
├── README.md
├── AGENTS.md
├── pyproject.toml
├── docker-compose.yml
├── app/
├── load_tester/
├── tests/
├── sample-data/
├── personas/
├── deploy/
└── docs/
```

## Coding Standards

- Add type hints to public functions.
- Use Pydantic models for request, config, and data validation where useful.
- Keep functions focused and short.
- Prefer dependency injection for testable components.
- Use structured logging instead of print statements in application code.
- Validate external input at boundaries.
- Raise clear exceptions with actionable messages.
- Write tests for ingestion, modeling, reporting, and guardrails.

## Security Rules

- Hash user identifiers during ingestion.
- Do not store raw user IDs in cleaned datasets.
- Do not commit real access logs.
- Use synthetic sample data only.
- Enforce maximum load test duration and concurrency.
- Use non root Docker containers where practical.
- Define Kubernetes resource requests and limits.

## Testing Requirements

Before considering a task complete, run:

```bash
ruff format .
ruff check .
pytest
```

For changes involving data models or reports, include focused unit tests.

## Documentation Requirements

When adding or changing behavior, update at least one of:

- `README.md`
- `docs/architecture.md`
- `docs/design-decisions.md`
- `docs/security-governance.md`
- `docs/demo-results.md`

Documentation should include commands, expected outputs, and troubleshooting notes when relevant.

## What Not to Do

- Do not expand the MVP into a full commercial load testing platform.
- Do not add Kubernetes complexity before the local flow works.
- Do not introduce a frontend unless the CLI and reports are already stable.
- Do not use real user data.
- Do not skip tests for core logic.
- Do not hide important setup steps in undocumented scripts.