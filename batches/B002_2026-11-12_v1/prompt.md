# Prompt — B002

- Date sent: <YYYY-MM-DD>
- Model: <model name>
- Skill version: <v1>
- Surface: <claude.ai / Claude Code / API>

## Exact prompt

Use the pair-discovery skill to propose a new batch of candidate pairs.

- Batch ID: B002
- As-of date T: 2026-11-12
- Formation window: 2023-11-12 to 2026-11-12
- Trading window: 2026-11-13 onward (never used for selection)
- Universe and liquidity floor: skill defaults (US-listed equities and ETFs, price > $5, median daily dollar volume > $5M over the formation window, listed for the whole formation window)
- Batch size: 25–30 candidates
- Mode: classify against your knowledge cutoff as the skill specifies. Web search only for current structural facts (ownership stakes, business mix, listing status), never prices, returns or spread behaviour.

Follow the skill's output format in full: run header, candidate table, screening spec with trial count N, the registry entry, the "Pairs (paste)" line, and the weakest-candidates note.
