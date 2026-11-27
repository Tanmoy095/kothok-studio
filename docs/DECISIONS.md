# Decisions

## 2026-11-27 — Brief overrides plan numbering and scope

- **Decision:** Follow the active brief's Phase 0–6 roadmap, product name
  Kothok, and own-voice-only rule.
- **Why:** The brief explicitly overrides disagreements in the older plan;
  the plan uses Phase 1–5 and the earlier Bangla Voice Studio naming.
- **Alternatives rejected:** Treating the plan as authoritative where it differs.

## 2026-11-27 — Start with a model-free mock

- **Decision:** Keep Phase 0 synthesis deterministic and offline with a
  standard-library WAV tone.
- **Why:** It gives tests a safe, model-free path while the named Bangla model
  and prefix remain unverified.
- **Alternatives rejected:** Loading or downloading the unverified model in CI.

## 2026-11-27 — Pin Gradio 6.28.0 for the scaffold UI

- **Decision:** Use the current Gradio 6.28.0 release with a direct pinned
  `requests` dependency.
- **Why:** A live launch with Gradio 5.20.1 failed while generating API schema;
  Gradio 6.28.0 passed schema generation and served the local UI.
- **Alternatives rejected:** Keeping the older pin that failed the Phase 0
  runtime smoke test.
