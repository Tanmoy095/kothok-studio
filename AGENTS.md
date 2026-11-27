# Kothok contributor guide

## Purpose

Kothok (কথক) is a free, local Bangla Voice Studio. Clone only the owner's own
voice. Never add impersonation features or commit personal recordings.

## Run and check

- First setup: double-click `setup.bat`.
- Start the UI: double-click `run.bat`.
- Checks: `scripts\check.bat` (Ruff and pytest; no model downloads).
- The Phase 0 preview is synthetic and is not a real TTS engine.

## Folder map

- `app.py`: Gradio entry point.
- `core/`: pipeline and engine adapters.
- `docs/`: architecture, decisions, progress, and operating notes.
- `tests/`: offline automated checks.
- `scripts/`: checks and generated figures.
- `library/`: locally supplied music/SFX and licence records.
- `requirements/`: pinned application and development dependencies.

## Standards

- Python 3.10+, type hints, pathlib, UTF-8, small documented modules.
- Keep config centralized; log under ignored `logs/`.
- Pin dependencies. Heavy engines use isolated environments.
- Do not invent model APIs, licences, benchmarks, or verified results.
- Use paths safely when the project folder contains spaces.

## Git

- One branch per phase (`phase/1-foundation`, etc.) or focused `fix/<name>`.
- Conventional Commit format: `type(scope): imperative summary`, <=72 chars.
- Include tests and docs with the behavior change. Do not commit if checks fail.
- Review each phase diff, create a PR, wait for CI, merge without squash, tag it.
- Never force-push main, rewrite published history, or use destructive cleanup.
- Never commit `voices/`, `models/`, `output/`, `projects/`, `.venv*/`, `logs/`,
  audio recordings, credentials, or `.env`.

## Verification

- Run unit tests and the model-free pipeline check.
- Run the actual UI and real engine when available; record commands and results.
- Measure audio properties before making audio-quality claims.
- Prepare human listening checks; do not claim naturalness without owner feedback.
- When a step cannot run, write the exact blocker to `docs/KNOWN_ISSUES.md`.

## Project memory

- [Master plan](docs/MASTER_PLAN.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Decisions](docs/DECISIONS.md)
- [Progress](docs/PROGRESS.md)
- [Next steps](docs/NEXT.md)
- [Known issues](docs/KNOWN_ISSUES.md)
- [Listening tests](docs/LISTENING_TESTS.md)
