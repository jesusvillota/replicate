---
id: TASK-003
title: OCR papers with PaddleOCR on cluster
milestone: M-1
state: draft
depends_on: []
delivery: pr
---

## Why

Serves SC-3: PaddleOCR output covers all three papers.

## Scope

Run PaddleOCR (https://github.com/PaddlePaddle/PaddleOCR) on the SLURM cluster (account `j-vill36`), with default tool settings. Never run model inference on the MacBook. The MacBook only submits the job, monitors it, and fetches results. Ship the three PDFs and the run script to shared storage (`/mnt/slurm-beegfs/Users/j-vill36/scripts_replicate/`). Before you submit, probe live capacity with `cluster-kit resources --json` and send the job to an unoccupied CPU partition that fits it. Keep at most one SLURM job of this task queued or running at a time (the account cap of 4 is shared with the three sibling tasks). Write output to `ocr/paddleocr/`, one file per paper. Out of scope: text cleanup, comparison with other methods, accuracy scoring.

## Acceptance

- `ocr/paddleocr/` holds one output file per input PDF (three files total).
- Each output file is non-empty and holds extracted paper text.
- The OCR ran on a cluster compute node, shown by the SLURM job ID, its `sacct` state, and a log tail in the outcome file.
- This task never held more than one cluster job queued or running at once.

## Verify

```sh
ls ocr/paddleocr/
wc -c ocr/paddleocr/*
sacct -j <job-id> --format=JobID,State,Elapsed,MaxRSS
```
