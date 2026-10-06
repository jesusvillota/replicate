# TASK-003 outcome

## Acceptance

- [ ] `ocr/paddleocr/` has one output file for each input PDF (three files total).
  The last remote listing showed only two files:
  - `Bessembinder_SSRN_2026_RebalancingFrictionalCostsAndReturnsToLeveredSingleStockETFs.txt` — 80,447 bytes.
  - `Bessembinder_SSRN_2026_VolatilityAndReturnsToLeveragedETFs.txt` — 42,508 bytes.
  I could not fetch them or confirm the third output after cluster SSH stopped working.
- [ ] Each output file is non-empty and contains extracted paper text.
  The two files above were non-empty. The runner checks for extracted text before it writes a file.
  I could not read the files or verify all three outputs locally.
- [ ] PaddleOCR ran on a cluster compute node, with the final SLURM state and log tail recorded.
  Job `23527` ran in `cpu_shared` on `HPCOM-01`. At the last remote check,
  `sacct` reported `RUNNING`, elapsed `01:41:12`. I lost SSH access before I could
  record its final state or final log tail. The last captured log tail was:

  ```text
  SLURM_JOB_ID=23527
  SLURM_JOB_PARTITION=cpu_shared
  SLURMD_NODENAME=HPCOM-01
  Started=2026-10-06T14:00:03+02:00
  Python 3.10.12
  paddlepaddle 3.3.1
  paddleocr 3.7.0
  ```
- [x] This task never held more than one cluster job queued or running at once.
  Accounting showed the earlier jobs ended before the next job was submitted:
  `23511` ended at 13:49:12; `23514` ended at 13:50:47; `23516` ended at
  13:52:03; and `23519` ended at 13:55:48. Job `23527` started at 14:00:02.
  No later task job was submitted. The last queue view showed `23527` as the only
  PaddleOCR task job.

## Blocked

Goal-Blocked: SSH to `192.168.1.61:22` is refused, so job `23527` and the third
output cannot be verified or fetched.

Cluster access is unavailable. Tailscale can reach `192.168.1.61`, but TCP port
22 refuses connections. `cluster-kit resources` and `cluster-kit exec` both fail
with the same SSH refusal. macOS reports the FortiClient VPN service as
disconnected. FortiClient's window shows its cloud management link as connected,
but no active remote-access VPN. I could not check job `23527`, read its final
log, or fetch the third output.

## Summary

The runner used PaddleOCR `3.7.0` and PaddlePaddle `3.3.1` on the cluster.
The OCR model and OCR settings stayed at their defaults. The job disables
Paddle's automatic oneDNN backend because the earlier oneDNN attempt failed.
This setting is `PADDLE_PDX_ENABLE_MKLDNN_BYDEFAULT=False` in the SLURM script.

The verified runner revision is `ce6590e`. Two remote output files existed at
the last check. Job `23527` was still running then. Its current state is unknown.

Follow-up: restore SSH access, check job `23527` and its log, fetch all three
outputs, run the required checks, and update this outcome and the draft PR.
