# TASK-002 outcome: OCR papers with Chandra

Status: blocked. No paper output was produced.

## Acceptance

- [ ] `ocr/chandra/` holds one output file per input PDF (three files total).
  Evidence: `ls ocr/chandra/` shows only `.gitkeep`. No paper file exists.
  The Verify command `wc -c ocr/chandra/*` reports only the 0-byte
  placeholder. Item fails.
- [ ] Each output file is non-empty and holds extracted paper text.
  Evidence: there is no output file, so there is no extracted text.
  Item fails.

## Summary

- What: I tried to run Chandra (`chandra-ocr` 0.2.0, default settings)
  locally on the three PDFs at the repo root, with output to `ocr/chandra/`.
- How: I created a virtual environment in the system temp dir, installed
  `chandra-ocr[hf]`, opened the draft PR, and started the local run
  (`chandra <pdf> ./output --method hf`, the only local method).
  The run must first download the `datalab-to/chandra-ocr-2` weights.
- Deviations: none from the spec. I did not use another tool. I stopped
  before writing any fake output, so `ocr/chandra/` still holds no paper text.
- Verified revision: `69edc2f` (init commit on `goal/ocr-papers/task-002`).
  Verify commands run: `ls ocr/chandra/` and `wc -c ocr/chandra/*`.
  Both confirm the blocked state above.
- Findings (why blocked):
  1. The weights download is large (a single partial blob already reached
     9.5 GB and was still incomplete). Free disk on this machine is about
     10-11 GB and keeps shrinking because sibling task workers share it.
     A full download risks filling the disk to zero.
  2. The test download later stalled at 0 B/s for 60 s while the machine
     load average sat above 9.
  3. The only other local method (`--method vllm`) needs a GPU vLLM server
     with Docker. This Mac has no such server.
  4. The managed Datalab API path needs an API key and credits. No key
     exists in this environment, and signup needs a human.
  5. A full local CPU run would still need to infer 136 pages
     (39 + 21 + 76) through a 32-layer vision-language model after the
     download. This exceeds what this shared machine can do now.
- Proposed follow-ups: see the decision request below. After the decision,
  resume this task with the resume note and run the Verify commands again.

## Decision request

Question: how shall TASK-002 obtain Chandra output for the three papers?

- Option A: provide a Datalab API key with credits, and allow the worker
  to send the three PDFs to the managed API. Trade-off: fast and accurate,
  but papers leave the machine and it costs credits.
- Option B: provide a machine with a GPU, free disk above 60 GB, and Docker,
  and run the local `chandra` CLI there with default settings.
  Trade-off: data stays local, but setup takes longer.
- Option C: drop Chandra from the goal (mark SC-2 out of scope).
  Trade-off: unblocks the goal, but the four-method comparison loses one
  method.

### Recommendation

Option A. It is the fastest path to real Chandra output, and the PDFs are
already public SSRN papers, so sending them to the API is low risk.
