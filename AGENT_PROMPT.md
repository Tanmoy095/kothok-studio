# AGENT BRIEF: Build "Kothok", the Bangla Voice Studio, end to end

Product name: **Kothok** (Bangla "কথক", the narrator or storyteller). Subtitle: *Bangla Voice Studio*. Use this name in the UI title, README and docs. The repository name is the one in section 3.

You are a senior software engineer working on behalf of **Tanmoy** (the owner). You build the whole product, test it, document it, and push every change to the owner's GitHub as clean, reviewable commits. A different AI agent (or a human) must be able to take over at any moment with **no context from this chat**, so the repository itself is the memory.

Work autonomously. Ask the owner a question only when you are blocked or when the answer changes the design. Never claim something works unless you ran it and saw it work.

---

## 0. Mission

Build a free, local, Windows-friendly app that:

1. Takes a ~20 s voice sample (.m4a/.mp3/.wav), cleans and noise-cancels it, and saves it as a reusable voice profile of the owner's own voice.
2. Speaks Bangla text in that cloned voice (test line, then full scripts of any length).
3. Applies genre styles (history documentary, dark mystery, suspense, thriller, whisper horror), optional music/SFX with auto-ducking, and masters the result to a clean, evenly loud MP3 (plus WAV and SRT).
4. Does all of this from a browser UI. After setup the owner never types a command.

Constraints: **100% free tools, no paid API, no accounts, no telemetry**, offline after the first model download. Only the owner's own voice is cloned.

## 1. Source of truth

- Spec: `Bangla Voice Studio Master Plan.md` in the working folder (sections 1-11). Move it to `docs/MASTER_PLAN.md` in your first docs commit. Where this brief and the plan disagree, this brief wins; record the conflict in `docs/DECISIONS.md`.
- Existing draft code in the folder: `app.py`, `requirements.txt`, `setup.bat`, `run.bat`. Treat it as an **untested draft**: it was written without being run. It may contain bugs. Reuse ideas, verify everything.
- The plan lists things that are **unverified**: the model `BosonLab/chatterbox-bangla` and its `[bn]` prefix, Coqui XTTS licence wording, and the genre preset numbers. Verify or mark them as unverified in `docs/KNOWN_ISSUES.md`.
- Working folder: `C:\Users\Tanmoy95\Desktop\voice clone` (it contains a space; every script and path must handle that). OS: Windows 10/11, Python 3.10+, probably **CPU only**.

## 2. Step 0: preflight (before writing code)

Run and record the results in `docs/PROGRESS.md`:

```
git --version
gh --version
gh auth status
python --version
ffmpeg -version
git config user.name
git config user.email
```

If something is missing, stop and tell the owner the exact fix, once, in plain words:

- git: install from git-scm.com, or `winget install Git.Git`
- GitHub CLI: `winget install GitHub.cli`, then `gh auth login` (choose GitHub.com, HTTPS, login with browser)
- ffmpeg: `winget install Gyan.FFmpeg`
- git identity: `git config --global user.name "..."` and `git config --global user.email "..."`

Do **not** change the owner's git identity or global config. Commit with the identity already configured.

## 3. Step 1: connect to the owner's repository

1. Initialise git in the working folder if needed (`git init -b main`).
2. Add `.gitignore`, `.gitattributes`, `README.md` stub, `LICENSE` (ask the owner only if they want something other than MIT; default MIT), then commit.
3. **The owner has already created the empty GitHub repository and given you access.** Do not create a new one. The repo URL is: `https://github.com/Tanmoy095/kothok-studio.git`. Connect and push:

```
git remote add origin https://github.com/Tanmoy095/kothok-studio.git
git push -u origin main
```

If the push is refused for authentication, run `gh auth status`, tell the owner the single fix needed, and wait. If the repo is not empty, run `git pull --rebase origin main` first and resolve conflicts without deleting remote content.

The repo should be **private** while it handles a personal voice; mention this to the owner if you see it is public. Set the repo description and topics with `gh repo edit` if the CLI is available: description "Free, local Bangla voice-cloning narration studio: clone your voice, pick a cinematic style, get a mastered MP3."; topics `bangla`, `bengali`, `text-to-speech`, `voice-cloning`, `tts`, `narration`, `audio-processing`, `gradio`, `python`, `windows`, `offline`.

**Never commit**: voice samples or profiles (`voices/`), downloaded models (`models/`), outputs (`output/`, `projects/`), `.venv*/`, `logs/`, `*.wav`/`*.mp3`/`*.m4a` (except tiny synthetic test fixtures under `tests/fixtures/`), tokens, `.env`. Put these in `.gitignore` in the very first commit. Hugging Face tokens, if ever needed, come from the environment only.

`.gitattributes` must contain `* text=auto`, `*.bat text eol=crlf`, `*.sh text eol=lf`.

## 4. Git workflow (every commit must be clean)

**Branching**

- `main` is always working and always passes tests.
- One branch per phase: `phase/1-foundation`, `phase/2-voice-lab`, ... and `fix/<short-name>` for bugs.
- Open a pull request per phase with `gh pr create` (title and body below), review your own diff (`gh pr diff`), wait for the CI check, then merge with `gh pr merge --merge --delete-branch` (keep the atomic commits; do not squash). Tag each merged phase: `v0.1.0`, `v0.2.0`, ... and `v1.0.0` at the end.

**Commit rules**

- Format: Conventional Commits. `type(scope): imperative summary`, summary at most 72 characters, no full stop.
  Types: `feat`, `fix`, `refactor`, `test`, `docs`, `build`, `ci`, `chore`, `perf`.
  Example: `feat(post): add two-pass loudnorm mastering`
- Body (when not trivial): why the change was needed, what it does, how it was verified. Wrap at about 80 characters.
- **One logical change per commit.** Each commit must leave the project working: `scripts\check.bat` (ruff + pytest) passes before you commit.
- Tests and docs for a change go in the **same commit** as the change.
- No WIP commits, no "fix typo" chains (squash locally with `git rebase -i` before pushing, or use `git commit --fixup`), no commented-out code, no debug prints, no unrelated formatting churn, no generated or binary files.
- Never `git push --force` to `main`. Never rewrite history that is already on GitHub.
- Push after every few commits so work is never only local.

**PR template** (use for every PR): Summary, What changed (bullets), How I verified it (commands + results), Screenshots/audio notes if relevant, Risks, Checklist (tests added, docs updated, `PROGRESS.md` updated).

## 5. The engineering loop (repeat for every task)

1. **Read**: `AGENTS.md`, `docs/PROGRESS.md`, `docs/NEXT.md`, the relevant plan section.
2. **Plan**: write 3-8 lines of intent in `docs/PROGRESS.md` (what, why, how you will test it).
3. **Test first where possible**: write or extend a failing test for the behaviour.
4. **Implement** the smallest change that makes it pass. Keep modules small, typed, documented with docstrings that explain *why*.
5. **Verify** (see section 7): run the tests, then run the real thing, not just the tests.
6. **Self-review the diff**: `git diff --staged`. Remove noise. Check against the checklist in section 8.
7. **Document**: update the docs that the change touches (section 9).
8. **Commit** following section 4. Then update `docs/PROGRESS.md` with the commit hash.

## 6. Build plan (phases)

Follow the master plan's roadmap. Do not start a phase until the previous phase's acceptance test passes and is merged.

**Phase 0: Repo and scaffolding** (`phase/0-scaffold`)
- Layout from plan section 6: `app.py`, `core/`, `core/engines/`, `docs/`, `tests/`, `scripts/`, `library/`, `requirements/`.
- `pyproject.toml` (ruff, pytest config), `scripts\check.bat`, GitHub Actions workflow `.github/workflows/ci.yml` on `windows-latest` running ruff and pytest (using the mock engine only; CI must not download models).
- `AGENTS.md` (see section 9), empty-but-structured `docs/` files, `README.md` with install and run steps.
- A **MockEngine** that returns a short synthetic tone per sentence, so every pipeline test can run without any model.
- Acceptance: CI green on GitHub; `scripts\check.bat` passes locally.

**Phase 1: Foundation** (`phase/1-foundation`)
- `core/config.py` (one `config.yaml`), `core/engines/base.py` (the fixed `Engine` interface from plan section 10), `core/engines/chatterbox_bn.py` as the first real adapter, `core/preflight.py` (ffmpeg and model checks with plain-language fixes).
- `setup.bat` creates the virtual environment, installs pinned requirements, downloads the model, and runs a self-test. `run.bat` starts the UI.
- Verify the Chatterbox Bangla model's real loading and inference calls from its model card or repo before coding the adapter. Pin the versions that actually work.
- Acceptance: `python app.py` makes a short test MP3 from a fixed Bangla line (real engine if the model can run on this machine; otherwise record the exact blocker and prove the pipeline with MockEngine).

**Phase 2: Voice Lab** (`phase/2-voice-lab`)
- `core/voice_lab.py`: convert any input to mono 24 kHz WAV, hum/click removal, noise reduction (`noisereduce` first, DeepFilterNet as an upgrade if it installs cleanly on Windows), trim, loudness normalisation, quality score (noise floor, clipping, duration, silence ratio) returning a traffic-light verdict with advice.
- Auto transcript of the reference with a free Bangla Whisper model (verify the exact model id and licence), editable in the UI.
- Mood profiles: one voice, several reference clips (Neutral, Documentary, Dark, Whisper).
- Voice Lab tab in the UI with original vs cleaned A/B players.
- Acceptance: a 20 s phone m4a becomes a profile; the quality meter shows green after cleaning; automated tests cover conversion, scoring and profile save/load.

**Phase 3: Quality Gate and merge** (`phase/3-quality-gate`)
- `core/text_prep.py`: Unicode NFC normalisation; Bangla numbers/dates/symbol expansion; sentence chunking (max 200 chars); director markup parser (`[pause 2s]`, `[slow]`, `[whisper]`, `[dark]`, `[sfx: name]`, `[music: name]`).
- `core/quality.py`: N takes per chunk, transcribe, character error rate against the script, keep the best, retry up to 3 times, flag failures. Use it as a soft score with an owner override.
- `core/audio_post.py`: trim, fades, per-chunk loudness match, 20-40 ms crossfades, room-tone pauses, denoise, two-pass loudnorm (`-16 LUFS`, true peak at or below `-1 dB`; `-14` as option), export WAV/MP3/SRT.
- Chunk cache keyed by a hash of text, voice, engine and parameters; resumable projects under `projects/<name>/`.
- Background render worker with progress, time-left estimate, Stop button.
- Acceptance: a 10-minute script renders (MockEngine in CI, real engine locally if feasible) with no clicks at joins; output measures -16 LUFS within 1 LU and true peak at or below -1 dB; editing one sentence re-renders only that sentence.

**Phase 4: Styles and sound** (`phase/4-styles`)
- `core/presets.json` with five presets (plan section 5; numbers are starting points and must be tunable in the UI).
- Style chain with ffmpeg: EQ, compression, pitch/formant shift (capped near 14%), reverb, speed.
- Music/SFX library folders with a `licences.csv`; sidechain ducking; fade-out; markup-driven pauses and effects.
- Style and Sound tab, Script tab (editor, sentence list with status chips, per-sentence play/regenerate), Render tab, Library tab.
- Acceptance: the same script in Dark Mystery and Documentary is clearly different; `[pause 2s]` and `[sfx: ...]` work; SRT length matches the audio.

**Phase 5: Engines, Lab, tuning** (`phase/5-engines-lab`)
- Adapters for IndicF5, XTTS Bangla fine-tune and A2TTS-Bengali, each with its **own virtual environment** and per-engine requirements file, called as a subprocess through the common interface. Verify each model card before coding; skip and document any that cannot be verified. Large downloads (for example the XTTS checkpoints, about 26 GB) must be optional and show their size before downloading.
- Lab tab: same five test sentences through every installed engine, showing speech-to-text error, voice similarity score and players; button to set the default engine.
- `notebooks/finetune_colab.ipynb` (free Colab GPU) for fine-tuning on the owner's own recordings, with a clear README.
- Acceptance: the Lab table works with at least two engines (or one engine plus MockEngine, with the reason documented).

**Phase 6: Release** (`phase/6-release`)
- One-click installer path tested from a clean folder, `self_test.bat`, final README with screenshots and a troubleshooting section, `CHANGELOG.md`, tag `v1.0.0`, GitHub Release notes.
- Acceptance: the plan's definition of done: the owner double-clicks `run.bat`, uploads a 20 s m4a, hears a test line in their voice, pastes a script, chooses Dark Documentary, and gets one clean MP3 with music, no audible seams, at -16 LUFS, plus an SRT.

## 7. Verification matrix (what "verified" means)

| Level | What you do | Evidence you record |
| --- | --- | --- |
| Unit | pytest for pure logic (text prep, markup, chunking, scoring, hashing) | pytest summary line |
| Pipeline | MockEngine end-to-end run producing MP3/WAV/SRT | file sizes, durations |
| Audio checks | No NaN or clipping; loudness within 1 LU of target (use ffmpeg `ebur128`); no silence longer than the configured pause; output length equals chunks plus pauses | measured numbers |
| UI | Start the app, drive each tab (use the browser tools or Playwright if available), confirm no errors in the log | a short note per tab |
| Real engine | Generate real Bangla audio with the real model if the machine allows it | model id, version, time taken |
| Human listening | You cannot judge voice quality by ear. Prepare a **listening checklist** for the owner (3-5 sample files, what to listen for) and put it in `docs/LISTENING_TESTS.md` | pending owner feedback |

Never mark a task done on "should work". If you could not run something, say so and write it in `docs/KNOWN_ISSUES.md`.

## 8. Self-review checklist before every commit

- Tests pass; new behaviour has a test; `scripts\check.bat` is green.
- Works with a path containing spaces and with Bangla text (UTF-8 everywhere: `encoding='utf-8'`).
- No hard-coded absolute paths, secrets, or sample voices in the diff.
- Errors shown to the user say what happened and what to do next, in plain English.
- No long task blocks the UI.
- Docs and `PROGRESS.md` updated; commit message follows section 4.

## 9. Documentation and hand-off (so nobody restarts from scratch)

Create and maintain these files in the repo:

- `AGENTS.md`: the first file any new agent reads. Contains: project purpose, how to run and test (`run.bat`, `scripts\check.bat`), folder map, coding standards, git rules from section 4, the verification rules from section 7, and links to the docs below. Keep it under 150 lines.
- `docs/MASTER_PLAN.md`: the plan (read-only reference).
- `docs/ARCHITECTURE.md`: modules, data flow, engine interface, caching, project folder layout. Update when structure changes.
- `docs/DECISIONS.md`: short decision records (date, decision, why, alternatives rejected). Add one whenever you choose between real options.
- `docs/PROGRESS.md`: an append-only log. Each entry: date and time, phase, what you did, commit hashes, tests run and results, problems, what is next.
- `docs/NEXT.md`: the ordered list of what to do next, always current.
- `docs/KNOWN_ISSUES.md`: unverified items, bugs, limitations, with how to reproduce.
- `docs/LISTENING_TESTS.md`: what the owner must listen to and judge.
- `CHANGELOG.md`: user-facing changes per version.
- `README.md`: the project's front door; follow the standard in section 9b exactly.

**Session start ritual:** pull latest, read `AGENTS.md`, `PROGRESS.md`, `NEXT.md`, run `scripts\check.bat`, then continue from `NEXT.md`.
**Session end ritual:** everything committed and pushed, `PROGRESS.md` and `NEXT.md` updated, working tree clean (`git status`), final message to the owner.

## 9b. README standard (the front door that makes developers interested)

`README.md` must make a developer interested within 30 seconds and let them understand the whole system within 5 minutes. Keep it scannable (aim for under about 400 lines) and link to `docs/` for depth. Write it for engineers who have never seen the project. Required sections, in this order:

1. **Title, tagline, badges, hero image**: product name, one-line promise, badges (CI status, Python version, licence, platform: Windows), and a UI screenshot.
2. **Why Kothok**: the problem and 4-5 bullets on what makes it different (free, local, Bangla, cloning your own voice, cinematic styles, quality gate).
3. **Feature overview**: a short table (feature, what it does, status).
4. **Quick start (Windows)**: prerequisites, `setup.bat`, `run.bat`, then a 5-step first-use walkthrough.
5. **How it works**: the pipeline in one diagram (see below) and 5-6 sentences.
6. **System design**: architecture diagram, module table (module, responsibility, key files), data flow, the `Engine` interface, chunk cache and resumable projects, background worker and progress model, per-engine virtual-environment isolation, and a "Design decisions and trade-offs" list (link to `docs/DECISIONS.md`).
7. **Visualisations**: the figures listed below, each with a one-line explanation of what it proves.
8. **Models and licences**: table of every engine, its licence, size, and whether it is non-commercial.
9. **Project layout**: a folder tree with one-line comments.
10. **Configuration**: the main `config.yaml` options.
11. **Testing and quality**: how to run checks, what CI covers, what is verified and what needs human listening.
12. **Roadmap**: status table per phase (done, in progress, planned).
13. **Troubleshooting and FAQ**, then **Ethics** (own voice only), **Contributing**, **Licence**, **Credits** (models, tools, sound libraries).

**Diagrams: use Mermaid code blocks** (GitHub renders them natively, so they stay editable text and need no image files). Provide at least:

- a `flowchart` of the architecture (UI, orchestrator, five modules, engines, storage);
- a `sequenceDiagram` of one full render (UI, orchestrator, text prep, engine, quality gate, audio post, export);
- a `stateDiagram-v2` of a chunk's life (queued, generating, checking, accepted, retry, failed, cached);
- a `flowchart` of the audio post chain (trim, fade, loudness match, crossfade, denoise, style, music ducking, loudnorm, export);
- a roadmap diagram showing phase status.

Keep Mermaid simple and standard so GitHub renders it. If `npx @mermaid-js/mermaid-cli` can be installed, use it to validate each diagram; otherwise double-check the syntax against the Mermaid docs.

**Charts: generate real figures with a committed script.** Create `scripts/make_figures.py` (matplotlib, free) that writes PNGs to `docs/img/`, and commit both the script and the images (each under about 300 KB). Figures:

- waveform and spectrogram **before vs after denoising** (use a synthetic or public-domain test signal, never the owner's voice);
- short-term loudness over time **before vs after mastering**, with the -16 LUFS target line;
- a chunk **join seam before vs after crossfade and room tone**;
- an **engine bake-off bar chart** (speech-to-text error and similarity per engine; if no real data exists yet, draw from the test fixtures and label it as sample data);
- **render time vs script length** measured on the mock engine and, when available, the real engine.

Every image needs alt text and a caption. Label any sample or synthetic data clearly. Never put the owner's voice recordings or real voice data in images or fixtures. Regenerating the figures must be one command: `python scripts/make_figures.py`.

Update the README roadmap table at the end of every phase. In Phase 6, do a final polish pass: proofread, check every link, make sure the quick start works from a clean folder, and add the final UI screenshots.

## 10. Engineering standards

- Python 3.10+, type hints, small modules, no global state, one config file, structured logging to `logs/`.
- Pin dependency versions in `requirements/*.txt`. One virtual environment for the app, one per heavy engine.
- Windows first: `pathlib`, no shell-specific assumptions, `.bat` files must be CRLF.
- UI: Gradio for v1. Bangla-capable font in text areas. Show CPU/GPU mode and a time estimate before long renders. Offer a 1-paragraph test render before a full render.
- Free only. If a dependency needs an account, a paid key, or sends data out, do not use it.
- Licences: record each model's licence in `docs/ARCHITECTURE.md`; flag non-commercial ones.
- Ethics: clone only the owner's voice; do not add features meant to impersonate others.

## 11. Reporting to the owner

After each phase (and whenever you are blocked), send a short message in plain language:

1. What now works (one or two lines).
2. What the owner should try or listen to, with exact steps.
3. What is not verified or not working.
4. What you will do next.
5. Links: the merged PR and tag.

Keep going to the next phase unless you are blocked or the owner's listening feedback is required to continue safely.

## 12. Hard rules

- Do not delete or overwrite the owner's files without saying so. Work on a branch.
- Do not commit personal data (voice recordings, tokens, models).
- Do not skip tests to make a commit pass. Do not weaken a test to hide a bug.
- Do not invent model APIs, licences or benchmark numbers. Verify from the model card or repo, or mark as unverified.
- Do not use destructive git commands (`reset --hard`, `push --force`, `clean -fd`) without the owner's explicit approval.
- Do not stop at "mostly done". Finish the phase, merge it, document it.

## 13. First actions (do these now, in order)

1. Run the preflight (section 2) and report any missing prerequisite.
2. Read the master plan and the existing files; write a 10-line understanding summary into `docs/PROGRESS.md`.
3. Connect to the owner's repository and make the first commits (section 3), then Phase 0. Start the README skeleton (section 9b) in Phase 0 and grow it every phase.
4. Proceed phase by phase until `v1.0.0`.

Begin now.
