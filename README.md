# job-hunt

One folder per job posting analyzed with the `job-hunt` skill, under `src/job_opps/<company><role>/`.

Each folder has:
- `posting.md`: link, logistics, sections, and exact-phrase keywords
- `match.md`: fit score, keyword-by-keyword status, rabbit holes, gap talking points
- `resume_bullets.md`: ATS-matched bullets with keyword coverage
- `side_projects.md`: projects to close the gaps
- `keyword_map.html` / `keyword_map.json`: the bubble diagram and its data

Regenerate a map: `python scripts/keyword_map.py src/job_opps/<folder>/keyword_map.json src/job_opps/<folder>/keyword_map.html`

## Index

| Saved | Company | Role | Fit | Status | Folder |
|---|---|---|---|---|---|
| 2026-10-25 | ElevenLabs | Forward Deployed Engineer | 7/10 | Prepping | [elevenlabsfde](src/job_opps/elevenlabsfde) |
