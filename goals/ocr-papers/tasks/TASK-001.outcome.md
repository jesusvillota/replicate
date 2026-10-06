# TASK-001 outcome: OCR papers with Marker

## Acceptance

- [x] `ocr/marker/` holds one output file per input PDF (three files total).
  Evidence: `ls ocr/marker/` shows exactly three files:
  `Bessembinder_SSRN_2026_RebalancingFrictionalCostsAndReturnsToLeveredSingleStockETFs.md`,
  `Bessembinder_SSRN_2026_VolatilityAndReturnsToLeveragedETFs.md`,
  `Harvey-Mazzoleni-Melone_SSRN_2026_TheUnintendedConsequencesOfRebalancing.md`.
- [x] Each output file is non-empty and holds extracted paper text.
  Evidence: `wc -c ocr/marker/*` gives 111594, 44952 and 231755 bytes
  (388301 total). Each file opens with its paper title, authors and abstract
  (e.g. "Volatility and Returns to Leveraged ETFs", Bessembinder; "The
  Unintended Consequences of Rebalancing", Harvey-Mazzoleni-Melone).

## Summary

- What: ran Marker with default settings on all three root PDFs, wrote one
  Markdown file per paper to `ocr/marker/`.
- How: `uvx --from marker-pdf marker_single <pdf> --output_dir ocr/marker`
  per PDF (Marker defaults; CPU device, no extra flags). Installed the missing
  `llama-server` binary via `brew install llama.cpp` first. Hoisted each
  `<paper>/<paper>.md` to `ocr/marker/<paper>.md` so the directory holds one
  file per paper, same base name, as the goal requires.
- Deviations: Marker also emits extracted figure JPEGs and a `_meta.json`
  sidecar per paper; these were dropped to keep the required one-file-per-paper
  layout. A few dangling figure image links remain in the Markdown; left as-is
  because text cleanup is out of scope.
- Verified revision: `c413dd4` plus this task's commit(s) on
  `goal/ocr-papers/task-001` (see PR).
- Proposed follow-ups: none; cleanup/comparison/scoring belong to later work,
  out of scope here.
