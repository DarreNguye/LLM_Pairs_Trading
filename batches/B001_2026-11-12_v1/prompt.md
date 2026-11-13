# Prompt — B001

- Date sent: 2026-11-12
- Model: Claude Opus 5.5 (high effort)
- Skill version: v1
- Surface: claude.ai incognito chat

## Exact prompt

Use the pair-discovery skill. Batch ID: B001.

- As-of date T: 2023-12-31. This is historical mode: your knowledge extends past T, so follow the skill's historical-mode rules (no web search) and label the output Historical-contaminated.
- Formation window: 2020-12-31 to 2023-12-31 (3 years ending at T).
- Trading window: 2024-01-01 to 2025-12-31.
- Universe: US-listed stocks only (no ETFs or closed-end funds), price between $5 and $1,000 at T, median daily dollar volume above $5M over the formation window, listed for the whole formation window.
- Batch size: 12 candidate pairs.

Return the full output format, including the registry entry with the `Pairs (paste):` line.
