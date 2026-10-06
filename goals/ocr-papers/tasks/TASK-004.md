---
id: TASK-004
title: OCR papers with paperextract
milestone: M-1
state: approved
depends_on: []
delivery: pr
route: {platform: opencode, model: opencode/muse-spark-1.3-contributor-free}
---

## Why

Serves SC-4: paperextract output covers all three papers.

## Scope

Run paperextract (https://github.com/jtravs/paperextract) with default settings on all three PDFs at the repo root. Write output to `ocr/paperextract/`, one file per paper. Out of scope: text cleanup, comparison with other methods, accuracy scoring.

## Acceptance

- `ocr/paperextract/` holds one output file per input PDF (three files total).
- Each output file is non-empty and holds extracted paper text.

## Verify

```sh
ls ocr/paperextract/
wc -c ocr/paperextract/*
```
