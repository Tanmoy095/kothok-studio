# Known issues and unverified items

- In the current Codex shell, Python/GitHub CLI/FFmpeg are not all on PATH.
  Python 3.13.17 and FFmpeg 9.1 were verified by full path/direct invocation.
- GitHub CLI 2.106.0 is installed, but `gh auth status` reports: `You are not
  logged into any GitHub hosts. To log in, run: gh auth login`. This blocks PR
  creation, merge, and private repository metadata checks through `gh`.
- `BosonLab/chatterbox-bangla` and its `[bn]` input prefix remain unverified.
- Coqui XTTS licence wording remains unverified.
- Genre preset parameter values are starting points only, not listening-tested.
- Phase 0 mock audio is a synthetic tone, not Bangla speech or a cloned voice.
