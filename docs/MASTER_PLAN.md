# Bangla Voice Studio: Master Plan

Nov 27, 2026 · @tanmoy

## 1. Goal and scope

Build a 100% free, local Windows app that clones your own Bangla voice from a 20-second sample and narrates long scripts in cinematic styles (suspense, thriller, dark, mystery, history documentary) with studio-clean output, using no paid APIs.

**Must-have outcomes**

- Upload a 20 s .m4a/.mp3, get a cleaned voice profile in one click.
- Paste or upload a full script and receive one finished MP3, no manual steps.
- Output sounds like one continuous take: no clicks between chunks, no volume jumps, no hiss.
- One-click genre styles with optional music and sound effects.
- Every component is free for personal use; licences are listed in section 2.

**Constraints**

- Hardware: you currently run CPU-only on Windows, so the plan has a CPU path and a free Google Colab GPU path.
- Voice is your own. Do not clone other people's voices without permission.

## 2. Research: free Bangla cloning models

No single free model is clearly best for Bangla, so the app should run several behind one interface and pick the winner by testing on your own voice. The base Chatterbox Multilingual model does not list Bengali among its 23 languages, so Bangla relies on community fine-tunes.

| Model | Bangla voice cloning | Needs | Licence / catch |
| --- | --- | --- | --- |
| [IndicF5 (AI4Bharat)](https://huggingface.co/ai4bharat/IndicF5) | Yes, zero-shot; Bengali is one of 11 Indian languages | 3-10 s reference clip plus its transcript; 330M parameters | Non-commercial restriction passes through from its training data |
| [Dhee-Indic-F5](https://huggingface.co/dheeyantra/dhee-indic-f5) | Yes; IndicF5 fine-tune aimed at steadier cloning from short references | Same inputs as IndicF5; noisy or very short references degrade output | Non-commercial |
| [XTTS v2 Bangla fine-tune (EMTIAZZ)](https://huggingface.co/EMTIAZZ/xtts-bangla-checkpoints) | Yes; 5 s reference, WAV or MP3 | About 26 GB of checkpoints; language is set to "en" as a tokenizer workaround | Coqui XTTS terms (non-commercial; from memory, verify) |
| Chatterbox Bangla fine-tunes: [Indic LoRA](https://huggingface.co/reenigne314/chatterbox-indic-lora) and the model in your original guide | Yes, but the LoRA's Bengali character error rate is high (0.245) | Chatterbox install; fast on GPU | Check each model card; I could not verify your BosonLab model |
| [A2TTS-Bengali / Sooktam2 (BharatGen)](https://aikosh.indiaai.gov.in/home/models/details/tts_with_spk_adapt_bengali.html) | Yes; speaker-adaptive diffusion model, about 150M parameters | Reference voice sample | MIT as listed |
| [Indic Parler-TTS (AI4Bharat)](https://huggingface.co/ai4bharat/indic-parler-tts) | No cloning; you describe the voice in words (pace, pitch, noise, reverb); Bengali emotion prompts are officially supported | Text description plus script | Apache 2.0 per a third-party listing; verify on the model card |
| BnTTS and [BanglaBox](https://arxiv.org/pdf/2610.09211) | Research systems; BanglaBox reports better 10 s zero-shot cloning than IndicF5 and the XTTS-v2 fine-tune | Check whether weights are public | Open question |

**Recommended stack.** Build a model adapter layer with one function, `speak(text, voice, style)`, and plug in IndicF5, the XTTS Bangla fine-tune and your Chatterbox model. Run a bake-off on the same five sentences in your voice, score each with an automatic Bangla speech-to-text check (section 4) plus your own ears, and make the winner the default. Indic Parler-TTS is a useful fourth engine for emotional delivery tests, but it cannot copy your voice.

**Licence note.** Everything here is free for personal use. If you ever monetise videos, re-check each model card: several are non-commercial.

## 3. Getting the best Bangla clone

The reference clip decides most of the quality, because these models copy tone and pacing as well as timbre. The cloning models in section 2 warn that noisy or very short references degrade output, so recording quality comes first.

**Recording checklist (20-30 s)**

- Record in a small, soft room (wardrobe, bedroom with curtains), mouth 15-20 cm from the mic, no fan or AC.
- Prefer a WAV at 44.1 or 48 kHz; an m4a from a phone works if the room is quiet.
- Read continuous, natural Bangla with clear pronunciation, no music, no long gaps, no clipping.
- Speak in the delivery you want copied. Record one clip per mood: Neutral, Serious documentary and Dark suspense. Each becomes its own voice profile.

**Features to add, ranked by gain per effort**

| Feature | What it does | Gain | Effort |
| --- | --- | --- | --- |
| Mood profiles | One voice, several reference clips (neutral, documentary, dark, whisper); the style picks the profile | High | Low |
| Reference quality check | Scores noise, clipping, length and silence before cloning, with a red/green verdict and tips | High | Low |
| Auto transcript of the reference | IndicF5-type models need the reference's text; a Bangla Whisper model fills it in and you correct it | High | Medium |
| Best-of-N takes | Generate 2-3 takes per sentence, transcribe each, keep the one closest to the script | High | Medium |
| Bangla text normaliser and pronunciation dictionary | Spells out numbers, dates, currency, abbreviations and English words as they should be spoken | High | Medium |
| Speaker-similarity score | Compares each take with your reference voice and rejects drifting takes | Medium | Medium |
| Fine-tune on your own voice | Train a small adapter on 30-60 minutes of your recordings using a free Colab GPU; the biggest long-term quality jump | Very high | High |

**Rule for the agent:** never judge a model by one sentence. Always compare engines on the same fixed test set of five sentences (short, long, numbers, questions, English words).

## 4. Merge, clean and master the full voice

The seams between chunks, uneven loudness and hiss are what make AI narration sound fake, so the pipeline fixes each chunk before joining and masters the whole file once at the end. Build it in this order:

1. **Prepare text.** Normalise numbers, dates and symbols to spoken Bangla, then split into sentence chunks of at most 200 characters. Mark paragraph breaks.
2. **Generate 2-3 takes per chunk.** Transcribe each take with a free Bangla Whisper model such as [BanglaSpeech2Text](https://pypi.org/project/BanglaSpeech2Text/0.0.18), compare it with the script, and keep the closest. If the error stays above a threshold after three tries, flag the sentence red in the UI so you can regenerate or edit it.
3. **Clean each chunk.** Trim leading and trailing silence, remove clicks and breaths at the edges, apply 10-20 ms fades, and match every chunk to the same loudness before joining. This removes volume jumps.
4. **Join with crossfades and room tone.** Use 20-40 ms crossfades and fill the designed pauses with very quiet room tone instead of digital silence, which sounds dead.
5. **Denoise the joined track.** Use [DeepFilterNet](https://arxiv.org/pdf/2305.08227) as the default: its authors report a real-time factor of 0.19 on a single-thread notebook CPU, so it suits your machine. Offer [Resemble Enhance](https://pypi.org/project/resemble-enhance/0.0.2.dev231215030627/) as an optional "Restore" button; it has a denoiser plus an enhancer that restores bandwidth, but it is heavier. Always keep an original-vs-cleaned A/B toggle, because heavy enhancement can add artefacts.
6. **Apply the genre style chain** (section 5): EQ, compression, pitch/formant shift, reverb.
7. **Mix music and effects** with sidechain ducking so the music dips under your voice and fades out at the end.
8. **Master with two-pass loudness normalisation.** Measure first, then apply linear gain, as [this FFmpeg loudnorm guide](https://dev.to/masonwritescode/two-pass-loudness-normalization-with-ffmpeg-loudnorm-the-right-way-1nm3) explains; single-pass loudnorm applies dynamic processing that can pump. Targets: -16 LUFS for podcasts, which [Apple's guidance](https://podnews.net/article/lufs-lkfs-for-podcasters) puts at a 1 LU tolerance with true peak no higher than -1 dB, or -14 LUFS for YouTube-style delivery.
9. **Export** a WAV master, a 192 kbps MP3, and an SRT subtitle file with timings taken from the chunk lengths, which saves hours in a video editor.

FFmpeg handles steps 3, 4, 6, 7 and 8, so the whole mastering stage is free and needs no extra install beyond what you already have.

## 5. Genre styles for suspense, thriller, dark mystery and history

Each genre is a preset of four things: which reference profile to clone, how the model is paced, how the audio is processed, and what music sits underneath. The numbers below are starting points to tune by ear, not tested values.

| Preset | Delivery | Pauses | Processing | Music and effects |
| --- | --- | --- | --- | --- |
| History documentary | Calm, authoritative, evenly paced; documentary reference clip | 0.5 s after sentences, 1.2 s after paragraphs | Warm EQ, gentle compression, light room reverb, speed about 0.95 | Slow orchestral or ambient bed about 22 dB below voice |
| Dark mystery | Low, measured, slightly slower; dark reference clip | 0.6 s sentences, 1.5 s paragraphs | Pitch/formant down 8-10%, bass lift, treble roll-off, medium reverb | Drone pad, distant wind, a single low piano note at reveals |
| Suspense | Quiet and controlled with rising intensity at the end of a scene | Long pause before each reveal (2-3 s) | Close-mic feel, less reverb, tight compression | Heartbeat or clock tick, slow riser before the reveal, silence at the reveal |
| Thriller | Faster, firmer, higher energy; shorter pauses | 0.2-0.3 s sentences, 0.6 s paragraphs | Presence boost around 3 kHz, tight compression, small room | Pulsing low synth, hits on scene changes |
| Whisper horror | Whispered or breathy reference clip; low expressiveness setting | 1-2 s | Slight high-pass, intimate dry sound, quiet reverb tail | Faint drone, creaks, single sting |

**Director markup.** Let the script carry instructions the app converts into audio, for example `[pause 2s]`, `[slow]`, `[whisper]`, `[dark]`, `[sfx: heartbeat]`, `[music: riser]`. A script can then control pacing and sound design without touching sliders, and it works for both single and long scripts.

**Sound design rules**

- Keep music about 20-25 dB under the voice and duck it automatically while you speak.
- Use silence deliberately: a 2-3 s gap before a reveal is stronger than any effect.
- Add one or two effects per scene, not many.
- Build a local sound library in folders such as `music/dark`, `music/documentary`, `sfx/heartbeat`.

**Free sources.** [Pixabay music](https://pixabay.com/music/search/liminal/) and [Freesound](https://freesound.org/people/kjartan_abel/sounds/558271) both list dark ambient, drone and cinematic tracks. Check the licence of every file you use: Freesound sounds carry per-file Creative Commons terms and some require attribution. Keep a `licences.csv` in the sound library with source, licence and URL for every file.

## 6. System architecture

One orchestrator runs five independent modules in order, so any module, especially the TTS engine, can be replaced without touching the rest.

&#91;embedded content: architecture · UI, orchestrator, 5 modules, storage\]

The quality gate (module 4) is the main addition over your current scripts: it checks and retries each sentence before anything is merged.

**Folder layout**

```
bangla-voice-studio/
  app.py                  UI entry point
  core/
    voice_lab.py          clean sample, quality score, transcript
    text_prep.py          normaliser, chunker, markup parser
    engines/              base.py, indicf5.py, xtts_bn.py, chatterbox_bn.py
    quality.py            Whisper check, best-of-N, similarity
    audio_post.py         merge, denoise, style chain, mix, master
    presets.json          genre styles
  library/                music/, sfx/, licences.csv
  voices/  models/        voice profiles and downloaded models
  projects/<name>/        script, chunks/, takes/, final/
```

**Design rules**

- Every engine implements the same interface: `load()`, `speak(text, reference, params)` and `sample_rate`.
- Cache each chunk by a hash of its text, voice, engine and settings. Editing one sentence re-renders only that sentence.
- Run long jobs in the background with a progress bar, and let a project resume after a crash.
- Keep all settings in one `config.yaml`, and log every run so bugs can be reproduced.

## 7. Planned UI

The UI is one browser page with five tabs that follow your workflow from left to right. Version 1 stays in Gradio (free, Python-only); move to a custom page only if you need the per-sentence editor to feel like a real app.

| Tab | Purpose | Key controls |
| --- | --- | --- |
| 1. Voice Lab | Turn a 20 s sample into a clean voice profile | Upload or record; noise-cancel strength; enhance toggle; quality meter (noise, clipping, length); auto transcript you can correct; original vs cleaned A/B player; mood label (Neutral, Documentary, Dark, Whisper); Save profile |
| 2. Script | Write and prepare the narration | Large text box or .txt upload; markup buttons (\[pause\], \[whisper\], \[sfx\], \[dark\]); word count and estimated duration; list of sentences with status chips (queued, ok, retry, failed) |
| 3. Style and Sound | Choose the genre look | Five preset cards; sliders for pace, depth, reverb, expressiveness; music picker with volume and ducking; loudness target (-16 or -14 LUFS); denoise engine (fast or restore) |
| 4. Render | Generate, watch, fix | Engine (auto or chosen); takes per sentence (1-3); Start and Stop; progress bar with time left; live log; per-sentence play, edit and regenerate; final player with MP3, WAV and SRT downloads |
| 5. Library | Keep everything | Projects (resume or duplicate); voice profiles; music and effects with licence column; past exports |
| Lab (advanced) | Compare engines | Runs the same five sentences through every engine and shows speech-to-text error, voice similarity and a player for each; button to set the winner as default |

**Render screen wireframe**

```
+-------------------------------------------------------------------+
| Voice [my_voice v]  Mood [Documentary v]  Engine [Auto v]         |
+----------------------------+--------------------------------------+
| SCRIPT                     | SENTENCES                            |
| [pause][whisper][sfx][dark]| 1 [OK]    ...text...      [play][redo]|
| (text editor)              | 2 [RETRY 2/3] ...text...  [play][redo]|
|                            | 3 [QUEUED] ...text...                 |
+----------------------------+--------------------------------------+
| Style: (Doc) (Mystery) (Suspense) (Thriller) (Whisper)            |
| Music [dark drone v] vol |----o----|     Loudness (x)-16 ( )-14    |
+-------------------------------------------------------------------+
| [Render 1 paragraph]  [Render full]   ######---- 62%  ~4 min left |
+-------------------------------------------------------------------+
| Result: [ player ]  [Download MP3] [WAV] [SRT]                    |
+-------------------------------------------------------------------+
```

**UI rules**

- Always offer a quick 1-paragraph test render before the full render.
- Show a plain-language fix whenever a step fails (for example "ffmpeg not found: run winget install Gyan.FFmpeg").
- Show whether the app is running on CPU or GPU, and the estimated time, before a long render starts.
- Support Bangla text everywhere, with a Bangla-capable font in the editor.

## 8. Roadmap and acceptance tests

Build in five phases and do not start the next one until the current phase's test passes. Phase 3 is where the quality jump happens, so protect time for it.

&#91;embedded content: roadmap · 5 phases, 5 gates\]

| Phase | Build | Acceptance test |
| --- | --- | --- |
| 1. Foundation | Move your current scripts into the folder layout; wrap your Chatterbox model as the first engine adapter | `python app.py` makes a test MP3 in your cloned voice; the ffmpeg check passes |
| 2. Voice Lab | Quality meter, noise cancel, auto transcript, mood profiles, A/B player | A 20 s phone m4a becomes a profile; the quality meter turns green after cleaning |
| 3. Quality Gate | Chunk cache, best-of-N, Whisper check, crossfade merge, per-chunk loudness match, DeepFilterNet, two-pass loudnorm | A 10-minute script renders with no clicks at the joins; the file measures -16 LUFS within 1 LU with true peak at or below -1 dB; editing one sentence re-renders only that sentence |
| 4. Styles | Five presets, markup parser, music library with ducking, effects, SRT export | The same script in Dark Mystery and Documentary sounds clearly different; `[pause 2s]` and `[sfx: heartbeat]` work; the SRT matches the audio length |
| 5. Lab and tune | Engine bake-off, similarity score, Colab fine-tune notebook | The bake-off table sets a default engine; the fine-tuned voice beats zero-shot on the five test sentences in your listening test |

## 9. Risks, licences and ethics

The biggest risks are Bangla model quality, CPU speed and conflicting Python packages, and each has a cheap mitigation.

| Risk | Why it matters | Mitigation |
| --- | --- | --- |
| No free model is good enough in Bangla | Community fine-tunes vary; one reports a Bengali character error rate of 0.245 | Engine bake-off on your voice; best-of-N takes; fine-tune on 30-60 min of your recordings |
| CPU is too slow for long scripts | Long scripts can run far slower than real time on CPU | Chunk cache, quick 1-paragraph tests, time estimate before render, free Colab GPU notebook for big jobs |
| Package conflicts on Windows | [IndicF5 setups pin](https://github.com/harrrshall/hinglish-tts) `transformers==4.49.0`, which may clash with other engines | One virtual environment per engine, called as a subprocess through the adapter interface |
| Speech-to-text check rejects good audio | Bangla ASR makes its own errors | Use it as a soft score, normalise Unicode and punctuation before comparing, and let you override |
| Over-enhancement adds artefacts | Heavy restoration can sound metallic | Light by default, A/B toggle, Restore is optional |
| Dark pitch shift sounds fake | Large shifts distort the voice | Cap the shift near 14%; prefer a dark-sounding reference clip over processing |
| Non-commercial model licences | Monetised videos could breach terms | Personal use now; re-check each model card before earning money; keep the MIT-listed Sooktam2 as a fallback to test |
| Sound-library licences | Some free tracks need attribution | Keep `licences.csv` with source, licence and URL for every file |

**Ethics.** Clone only your own voice. The IndicF5 model card [states](https://github.com/samnaveenkumaroff/Indic-F5) that you agree to clone only voices you have explicit permission for. Label AI-narrated content where a platform asks for it.

## 10. Instructions for the AI coding agent

Copy everything in this section into your coding agent as its brief. It assumes the agent can read this whole document.

**Role.** You are a senior engineer building Bangla Voice Studio for one user on Windows. The user is not a programmer, so the result must install with one `setup.bat`, start with one `run.bat`, and never require manual command steps.

**Starting point.** The user already has `app.py` (a Gradio app with voice cleaning, five style presets, chunked generation and ffmpeg post-processing), `requirements.txt`, `setup.bat` and `run.bat` in `C:\Users\Tanmoy95\Desktop\bangla-tts-win`, built around `BosonLab/chatterbox-bangla`. Read these files first and refactor them into the folder layout in section 6 without losing any working feature.

**Non-negotiable rules**

1. Everything must be free and offline after the first model download. No paid API, no account-gated service, no telemetry.
2. Windows first: use `pathlib`, UTF-8 everywhere, and test every path with spaces. Check that `ffmpeg` exists at start-up and show the exact install command (`winget install Gyan.FFmpeg`) if it is missing.
3. Bangla text must survive every step. Never use a default encoding; open files with `encoding='utf-8'`; keep Unicode normalisation (NFC) consistent before comparing texts.
4. Do not trust model names or APIs from memory. Before writing code for an engine, open its model card or repository, confirm the real loading and inference calls, and pin the working package versions in a per-engine requirements file. If a model cannot be verified, say so and skip it. The `BosonLab/chatterbox-bangla` model and its `[bn]` prefix are unverified.
5. Isolate engines. Each engine runs in its own virtual environment as a subprocess behind the common interface, so conflicting pins (for example `transformers`) cannot break the app.
6. Never block the UI. Run renders in a background worker with a progress bar, a Stop button and resumable chunk cache.
7. Every error shown to the user must say what happened and what to do next, in plain English.
8. Clone only the user's own voice. Do not add features that help impersonate other people.

**Engine interface (fixed contract)**

```python
class Engine:
    name: str
    sample_rate: int
    def load(self) -> None: ...
    def speak(self, text: str, reference_wav: str, reference_text: str | None,
              params: dict) -> "np.ndarray": ...   # mono float32 at sample_rate
```

Build adapters in this order: Chatterbox (the current model), IndicF5, XTTS Bangla fine-tune, then A2TTS-Bengali. Add Indic Parler-TTS only as an optional style-test engine without cloning.

**Build order.** Follow the phases in section 8 exactly. At the end of each phase: run the acceptance test, record the result in `docs/progress.md`, and stop for the user's approval before starting the next phase.

**Pipeline requirements** (sections 3-5)

- Voice Lab: quality score (noise floor, clipping, duration, silence ratio), noise cancel, DeepFilterNet default with optional Resemble Enhance, auto transcript with a Bangla Whisper model, editable, mood profiles.
- Text prep: normalise Bangla numbers, dates and symbols; sentence chunks of at most 200 characters; parse the director markup `[pause Ns]`, `[slow]`, `[whisper]`, `[dark]`, `[sfx: name]`, `[music: name]`.
- Quality gate: N takes per chunk, transcribe each, score character error rate against the script, keep the best, retry up to 3 times, flag failures.
- Audio post: trim, fade, match chunk loudness, 20-40 ms crossfade, room-tone pauses, denoise, style chain, music with sidechain ducking, two-pass loudnorm to the chosen target, export WAV, MP3 and SRT.
- Cache each chunk by a hash of text, voice, engine and parameters.

**Testing.** Create a `tests/` folder with a fixed set of five Bangla test sentences (short, long, numbers, question, English word). Add automatic checks: no NaN or clipping in output, loudness within 1 LU of target, no silence longer than the configured pause, output length equals the sum of chunks plus pauses. Provide a one-click `self_test.bat`.

**Coding standards.** Python 3.10 or newer, type hints, small modules, one config file, no global state, docstrings that explain why. Log to `logs/`. Pin dependency versions.

**Working protocol.** Before each phase, write a short plan; ask the user a question only when the answer changes the design; make the smallest change that satisfies the acceptance test; and report in plain language what works, what does not, and what the user must do next.

**Definition of done.** The user double-clicks `run.bat`, uploads a 20-second m4a, hears a test line in their own voice in under one minute of clicking, pastes a script, chooses Dark Documentary, and gets one clean MP3 with music, no audible seams, and loudness at -16 LUFS, plus an SRT file.

## 11. Sources

Researched on 27 Nov 2026 from search-result pages; I did not open every page in full, so confirm licences and install steps on each model card before relying on them.

| Topic | Source |
| --- | --- |
| IndicF5 model and cloning terms | [ai4bharat/IndicF5](https://huggingface.co/ai4bharat/IndicF5), [Indic-F5 repo](https://github.com/samnaveenkumaroff/Indic-F5) |
| IndicF5 fine-tune and non-commercial note | [Dhee-Indic-F5](https://huggingface.co/dheeyantra/dhee-indic-f5) |
| IndicF5 install pins and 3-10 s reference | [hinglish-tts repo](https://github.com/harrrshall/hinglish-tts) |
| XTTS v2 Bangla fine-tune | [EMTIAZZ/xtts-bangla-checkpoints](https://huggingface.co/EMTIAZZ/xtts-bangla-checkpoints), [BnTTS paper](https://arxiv.org/pdf/2502.05729) |
| BanglaBox research system | [arXiv 2610.09211](https://arxiv.org/pdf/2610.09211) |
| Chatterbox Multilingual language list | [Resemble AI model card](https://huggingface.co/ResembleAI/chatterbox/blob/main/README.md), [supported languages](https://www.mintlify.com/yocxy2/chatterboxyocxy/api/supported-languages) |
| Chatterbox Bengali LoRA | [reenigne314/chatterbox-indic-lora](https://huggingface.co/reenigne314/chatterbox-indic-lora) |
| A2TTS-Bengali / Sooktam2 | [AIKosh model page](https://aikosh.indiaai.gov.in/home/models/details/tts_with_spk_adapt_bengali.html) |
| Indic Parler-TTS | [ai4bharat/indic-parler-tts](https://huggingface.co/ai4bharat/indic-parler-tts) |
| Denoising and enhancement | [DeepFilterNet paper](https://arxiv.org/pdf/2305.08227), [Resemble Enhance](https://pypi.org/project/resemble-enhance/0.0.2.dev231215030627/) |
| Bangla speech-to-text for quality checks | [BanglaSpeech2Text](https://pypi.org/project/BanglaSpeech2Text/0.0.18) |
| Loudness targets | [FFmpeg loudnorm two-pass guide](https://dev.to/masonwritescode/two-pass-loudness-normalization-with-ffmpeg-loudnorm-the-right-way-1nm3), [Podnews LUFS guide](https://podnews.net/article/lufs-lkfs-for-podcasters) |
| Free sound libraries | [Pixabay music](https://pixabay.com/music/search/liminal/), [Freesound](https://freesound.org/people/kjartan_abel/sounds/558271) |

**Not verified:** the `BosonLab/chatterbox-bangla` model and its `[bn]` prefix, the Coqui XTTS licence wording, and the genre preset values in section 5.
