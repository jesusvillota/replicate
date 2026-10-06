---
id: TASK-001
title: OCR papers with Marker
milestone: M-1
state: draft
depends_on: []
delivery: pr
---

## Why

Serves SC-1: Marker output covers all three papers.

## Scope

Run Marker (https://github.com/datalab-to/marker) with default settings on all three PDFs at the repo root. Write output to `ocr/marker/`, one file per paper. Out of scope: text cleanup, comparison with other methods, accuracy scoring.

## Acceptance

- `ocr/marker/` holds one output file per input PDF (three files total).
- Each output file is non-empty and holds extracted paper text.

## Verify

```sh
ls ocr/marker/
wc -c ocr/marker/*
```
