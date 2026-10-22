---
id: TASK-002
title: Set up WRDS login on the MacBook
milestone: M-1
state: approved
depends_on: []
delivery: manual
priority: 1
route: {platform: codex, model: gpt-6-astra, effort: high}
---

## Why

Serves SC-1 and SC-2. TASK-010 reads WRDS from the MacBook, so it needs a WRDS login that works without a prompt. Today no `~/.pgpass` exists. This is a human step: WRDS needs your password and a Duo approval.

## Scope

The owner does these steps on the MacBook, never on the cluster:

1. Create `~/.pgpass` with one line, `wrds-pgdata.wharton.upenn.edu:9737:wrds:<username>:<password>`. Then run `chmod 600 ~/.pgpass`.
2. Add `export WRDS_USERNAME=<username>` to `~/.zshrc`, and open a new shell.
3. Run the Verify command once interactively, and approve the Duo push if WRDS asks for it.

Out of scope: any data extraction. That is TASK-010.

## Acceptance

- In a new shell, the Verify command prints a library count with no password prompt.

## Verify

```sh
uv run --no-project --with wrds python3 -c "import wrds; db = wrds.Connection(); print(len(db.list_libraries()), 'libraries')"
```
