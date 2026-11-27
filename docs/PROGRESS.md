# Progress log

## 2026-11-27 12:44 Asia/Dhaka — Phase 0 scaffold started

### Ten-line understanding summary

1. Kothok is a free, local Windows browser app for Bangla narration.
2. Voice cloning is limited to the owner's own recordings.
3. The target flow is sample cleanup, voice profile, script, style, mastered exports.
4. Gradio is the planned first UI, with setup and launch through batch files.
5. Python 3.10+ and FFmpeg are intended local prerequisites.
6. Real TTS adapters must share a small engine interface.
7. Mock synthesis must let CI exercise the pipeline without model downloads.
8. Personal audio, models, outputs, logs, and credentials must never be committed.
9. Model cards, licences, quality numbers, and preset values must be verified or flagged.
10. Human listening remains necessary for voice similarity and naturalness.

### Preflight

- `git --version`: `git version 2.51.1.windows.1` (available).
- `gh --version`: command not found; `gh auth status` could not run.
- `python --version`: command not found; `py` also unavailable.
- `ffmpeg -version`: WinGet link exists but fails to launch.
- `git config user.name`: `Tanmoy095`.
- `git config user.email`: `adtanmoy95@gmail.com`.
- GitHub repo is connected and `main` was pushed by the owner; origin points to
  `https://github.com/Tanmoy095/kothok-studio.git`.

### Intent for Phase 0

- Add ignore rules, line-ending policy, project metadata, CI, and a small mock engine.
- Establish tests and docs that work without any model download.
- Run the local check script and browser smoke test when Python is available.
- Review and commit the phase only after its required checks pass.

### Work performed

- Moved the supplied plan to `docs/MASTER_PLAN.md`.
- Added scaffold files, starter README, and a model-free mock engine on
  `phase/0-scaffold`.
- `cmd /c scripts\check.bat`: blocked immediately because `python` is not
  recognized; Ruff and pytest did not run.
- UI smoke test: not run for the same missing Python prerequisite.
- `git diff --check`: passed for tracked changes; all three batch scripts were
  inspected and contain CRLF line endings without bare LF endings.
- Commit: pending. Phase 0 acceptance and PR/CI workflow remain incomplete.
- Next: install Python 3.10+, working FFmpeg, and GitHub CLI; run local checks,
  then complete Phase 0 review and CI before starting Phase 1.

## 2026-11-27 13:00 Asia/Dhaka — Phase 0 re-verification

- Git: `git version 2.51.1.windows.1`; configured identity is `Tanmoy095`
  / `adtanmoy95@gmail.com`; origin is the expected `kothok-studio` repository.
- Host Python: `Python 3.13.17` at the owner-reported Python313 path.
- GitHub CLI: `gh version 2.106.0`; auth status says no GitHub hosts are logged in.
- FFmpeg: `9.1-full_build-www.gyan.dev`; direct `ffmpeg -version` succeeds.
- `setup.bat`: created/updated `.venv` and installed pinned dependencies.
- `scripts\check.bat`: Ruff passed; pytest `2 passed`.
- Live UI: `run.bat` started Gradio 6.28.0; `GET http://127.0.0.1:7860/`
  returned HTTP 200, Kothok title present, 15,764 response bytes. Server stopped.
- Fixed two issues discovered in verification: check script now uses `.venv`,
  and Gradio dependencies now match the successful live UI environment.
- `git fetch origin`: complete; `phase/0-scaffold` is based on `4422bc3`.
- Commit: pending. PR and CI are blocked until GitHub CLI is authenticated.
- Next: inspect staged changes, commit, push, authenticate `gh`, create/review
  the Phase 0 PR, and wait for CI.
- Final privacy rerun after the staged review: `run.bat` again returned HTTP 200
  with the Kothok title (15,765 bytes); analytics disabled and share links
  explicitly off. Ruff passed and pytest reported `2 passed` after this change.
- The mock engine test writes to a directory containing spaces. Batch files
  retain CRLF line endings.
