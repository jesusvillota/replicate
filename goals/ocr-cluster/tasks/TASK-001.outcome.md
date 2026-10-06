# TASK-001 outcome

## Acceptance

- [ ] `ocr/marker/` holds one output file per input PDF. Evidence: the cluster output folder is empty. The local `ocr/marker/` folder has no files.
- [ ] Each output file is non-empty and holds paper text. Evidence: no output file exists.
- [x] OCR ran on a cluster compute node. Evidence: `scontrol show job -o 23536` reported `NodeList=HPCOM-05`. `sacct` recorded state `CANCELLED by 1009`, elapsed time `00:16:35`, and peak memory `6604072K`. The log tail below shows stalled model work and canceled tasks. The job did not finish.
- [x] This task held at most one queued or running SLURM job at a time. Evidence: the table below lists every `marker-t001` job. Each job ended before the next one started.

### SLURM job history

Times use the cluster's local time on 2026-10-06.

| Job ID | Start | End | State |
| --- | --- | --- | --- |
| 23508 | 13:46:22 | 13:46:22 | CANCELLED |
| 23509 | 13:48:19 | 13:48:19 | CANCELLED |
| 23518 | 13:53:32 | 13:53:33 | FAILED |
| 23521 | 13:56:07 | 13:56:08 | FAILED |
| 23526 | 13:58:32 | 14:00:39 | FAILED |
| 23529 | 14:11:02 | 14:11:59 | FAILED |
| 23530 | 14:13:32 | 14:53:35 | CANCELLED |
| 23533 | 14:55:29 | 14:55:29 | CANCELLED |
| 23534 | 14:57:33 | 14:57:33 | CANCELLED |
| 23535 | 14:58:06 | 14:58:06 | FAILED |
| 23536 | 14:58:59 | 15:15:35 | CANCELLED |

### SLURM and log evidence

```text
$ sacct -j 23536 --format=JobID,State,Elapsed,MaxRSS
23536       CANCELLED by 1009  00:16:35  6604072K
23536.batch CANCELLED          00:16:36  6604072K
```

The compute-node log tail from `/mnt/slurm-beegfs/Users/j-vill36/.cache/datalab/surya/llamacpp_server.log` is:

```text
7.58.206.324 W find_slot: non-consecutive token position 79 after 7 for sequence 7 with 7 new tokens
8.06.512.254 I slot print_timing: id  2 | task 6 | prompt processing, n_tokens =      7, progress = 0.00, t = 480.59 s / 0.01 tokens per second
10.04.883.980 W srv          stop: cancel task, id_task = 3
10.04.919.899 W srv          stop: cancel task, id_task = 6
10.04.925.223 W srv          stop: cancel task, id_task = 4
10.04.942.195 W srv          stop: cancel task, id_task = 2
10.05.033.246 W srv          stop: cancel task, id_task = 0
10.05.074.338 W srv          stop: cancel task, id_task = 5
```

Job `23530` also logged six `Inference error: Request timed out.` messages before cancellation. No output file was produced by either job.

## Summary

The task staged the three input PDFs and the run script on shared storage. Marker ran on CPU node `HPCOM-05`. The run used Marker’s default `marker_single` conversion command and processed one PDF at a time.

The script selected Surya's `llamacpp` backend because the default backend required Docker. The cluster does not have Docker. The CPU model did not finish within the available CPU allocation. Job `23530` timed out. Job `23536` used four CPUs but still produced no output. Its log showed 480.59 seconds of model prompt processing for seven tokens, then canceled six tasks.

No output file was copied to the worktree. The shared output folder is empty. No task jobs overlapped. `bash -n scripts/run_marker_ocr.sh` passes. `gh pr checks 4` reports no checks. Verified revision before this outcome: `ff7deb36505dd7ca8b712468fbd0f205d1e4b79d`.

Follow-up: receive the decision below, then rerun with the approved cluster settings and complete the file checks.

## Decision request

May TASK-001 use a GPU partition, or change CPU inference settings, after the default CPU run times out?

Options:

1. Keep the CPU partition and current inference settings. Wait for a larger CPU slot, then retry. This keeps the task scope and defaults. The current CPU capacity produced no paper text.
2. Use a GPU partition with a GPU-enabled `llama.cpp` build. This may finish sooner and keeps Marker’s conversion command. It changes the task's CPU-only requirement and needs a GPU-compatible build.
3. Keep the CPU partition and tune `llama.cpp` threads, parallel requests, or timeouts. This may use current CPU capacity better. It changes the current inference settings and may not finish faster.

### Recommendation

Allow option 2. The current CPU runs produce no output and show very slow model work. A GPU-enabled backend offers the best chance of completing all three papers while keeping Marker’s conversion command at its default.
