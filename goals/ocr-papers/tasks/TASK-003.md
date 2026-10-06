---
id: TASK-003
title: OCR papers with PaddleOCR
milestone: M-1
state: approved
depends_on: []
delivery: pr
route: {platform: opencode, model: opencode/muse-spark-1.3-contributor-free}
---

## Why

Serves SC-3: PaddleOCR output covers all three papers.

## Scope

Run PaddleOCR (https://github.com/PaddlePaddle/PaddleOCR) with default settings on all three PDFs at the repo root. Write output to `ocr/paddleocr/`, one file per paper. Out of scope: text cleanup, comparison with other methods, accuracy scoring.

## Acceptance

- `ocr/paddleocr/` holds one output file per input PDF (three files total).
- Each output file is non-empty and holds extracted paper text.

## Verify

```sh
ls ocr/paddleocr/
wc -c ocr/paddleocr/*
```
