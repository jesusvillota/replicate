---
id: TASK-002
title: OCR papers with Chandra
milestone: M-1
state: approved
depends_on: []
delivery: pr
route: {platform: opencode, model: opencode/muse-spark-1.3-contributor-free}
---

## Why

Serves SC-2: Chandra output covers all three papers.

## Scope

Run Chandra (https://github.com/datalab-to/chandra) with default settings on all three PDFs at the repo root. Write output to `ocr/chandra/`, one file per paper. Out of scope: text cleanup, comparison with other methods, accuracy scoring.

## Acceptance

- `ocr/chandra/` holds one output file per input PDF (three files total).
- Each output file is non-empty and holds extracted paper text.

## Verify

```sh
ls ocr/chandra/
wc -c ocr/chandra/*
```
