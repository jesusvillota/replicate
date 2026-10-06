# TASK-001 outcome

## Acceptance

- [ ] `ocr/marker/` holds one output file per input PDF. Evidence: the local output folder is empty. Cluster sync and fetch did not run.
- [ ] Each output file is non-empty and holds extracted paper text. Evidence: no output files exist.
- [x] Marker ran on a cluster compute node. Evidence: SLURM job `23536` ran on `HPCOM-05`. Its `sacct` state and log tail appear below. The job was canceled and produced no output.
- [x] This task held at most one queued or running SLURM job at a time. Evidence: the job history below shows each job ended before the next started. This resume submitted no job.

## Previous SLURM job history

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

## SLURM and log evidence

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

Job `23530` also logged six `Inference error: Request timed out.` messages. Neither job produced an output file.

## Current blocker

DEC-001 was accepted on 2026-10-06. It allows a GPU partition or tuned CPU inference settings. The updated runner requests one L4 GPU, two CPUs, and 16 GB on `gpu_compute`. It uses a CUDA-enabled llama.cpp build and writes Markdown files directly to `ocr/marker/`.

The cluster became unreachable before this resume could sync or submit the updated runner. `cluster-kit resources --json`, `cluster-kit exec 'hostname'`, and the code sync all failed with `ssh: connect to host 192.168.1.61 port 22: Connection refused`. The FortiClient VPN stayed disconnected after a start attempt. No job was submitted in this resume, and no output was fetched.

## Summary

The existing PR already contains the runner and the failed CPU run history. This resume updates the runner for a one-GPU `gpu_compute` run and keeps the task job cap at one. The runner passes `bash -n`, and the changes pass `git diff --check`. No cluster run or output check could be completed because SSH access was unavailable.

Verified revision before this outcome commit: `e524bfd1f0ad13bacae9d9a473193ba742181cf0`.

Follow-up: restore cluster SSH access, sync the runner, run one `gpu_compute` job, fetch the three Markdown outputs, and update this outcome with the successful job evidence.
