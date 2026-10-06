# TASK-001 outcome

## Acceptance

- [ ] `ocr/marker/` holds one output file per input PDF (three files total). Evidence: the directory was empty on 2026-10-07; no Marker job was accepted in this resume.
- [ ] Each output file is non-empty and holds extracted paper text. Evidence: there are no output files to inspect.
- [x] Marker ran on a cluster compute node. Evidence: earlier job `23536` ran on `HPCOM-05`. Its `sacct` state and compute-node log tail appear below. That run was cancelled and produced no output. This resume's submission was rejected and received no job ID.
- [x] This task never held more than one queued or running SLURM job at a time. Evidence: the task's previous job history below is sequential. The current submission was rejected, so this resume held no task job.

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

Earlier job `23536`:

```text
$ sacct -j 23536 --format=JobID,State,Elapsed,MaxRSS
23536       CANCELLED by 1009  00:16:35  6604072K
23536.batch CANCELLED          00:16:36  6604072K
```

Compute-node log tail from `/mnt/slurm-beegfs/Users/j-vill36/.cache/datalab/surya/llamacpp_server.log`:

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

## Current capacity blocker (2026-10-07)

The runner now requests two CPUs, 10G, and one L4 GPU on `gpu_compute`. The three PDFs and runner were staged under this worktree's isolated remote path, `/mnt/slurm-beegfs/Users/j-vill36/scripts_replicate__goal-ocr-cluster-task-001/`.

The default `cluster-kit resources --json` probe showed an empty queue because its default SLURM username did not match the job owner. Querying with `cluster-kit resources --user j-vill36 --json` showed four running jobs: `23575`, `23576`, `23577`, and `23589`. `sacctmgr` reported `MaxJobs=4` and `MaxSubmit=4`. The free GPU node slot fit the requested job, but the account limit was full.

The attempted `sbatch --parsable scripts/run_marker_ocr.sh` returned:

```text
sbatch: error: AssocMaxSubmitJobLimit
sbatch: error: Batch job submission failed: Job violates accounting/QOS policy (job submit limit, user's size and/or time limits)
```

SLURM returned no job ID. No retry was made. A related `cluster-kit resources` username mismatch was recorded with `agent-note` outside this task.

## Summary

This resume reduced the runner's memory request from 16G to 10G and staged the inputs and runner on the cluster. The cluster node had a fitting 2 CPU, 10G, 1 GPU slot, but four other jobs already used the account's four-job limit. SLURM rejected the submission, so this resume produced no OCR outputs.

`bash -n scripts/run_marker_ocr.sh` and `git diff --check` passed. The output directory check found no files. No OCR verification could be completed in this resume.

Verified revision before this outcome update: `b2081d8`.

Follow-up: after an account job ends, query resources with `--user j-vill36`, then run one `gpu_compute` job with two CPUs, 10G, and one GPU. Fetch the three Markdown files and replace this blocker with the resulting `sacct` and log evidence.
