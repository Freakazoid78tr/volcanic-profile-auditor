---
name: secret-state-scan
description: Use when checking a public profile or repo for accidental secrets, private Hermes state, wallets, logs, sessions, memories, auth files, local databases, and risky runtime artifacts before publication or install.
version: 1.0.0
author: Volcanic
license: MIT
metadata:
  hermes:
    tags: [security, secrets, audit, hermes, profiles]
    related_skills: [profile-repo-inspection]
---

# Secret and State Scan

## Overview

Public profile repositories should contain reusable configuration and skills, not private runtime state. This skill defines what to check before publishing or installing a Hermes profile distribution.

## Red Flags

Flag these if present:

- `.env`, `.env.local`, `.env.production`
- `auth.json`, OAuth tokens, browser cookies
- `state.db`, `state.db-shm`, `state.db-wal`, SQLite runtime DBs
- `memories/`, `sessions/`, `logs/`
- `workspace/`, browser screenshots, local caches
- wallets, keystores, private keys, mnemonics, seeds
- API keys such as `sk-...`, `ghp_...`, or provider-specific tokens
- personal/private prompt files not intended for release

Allowed examples:

- `.env.EXAMPLE` with empty values
- public README and install instructions
- placeholder variable names
- audited scripts that do not contain credentials

## Workflow

1. Inspect file names and directories first; many leaks are obvious from names.
2. Search text files for common secret patterns and private-state words.
3. Read `.gitignore` to confirm future accidental files are blocked.
4. If a scanner script exists, inspect it before running it.
5. Report exact paths for problems. Do not print secret values in full.
6. Recommend deletion and history cleanup if secrets were already committed.

## Publication Checklist

Before a public profile repo is published:

- [ ] `.env` and auth files absent
- [ ] sessions/memories/logs absent
- [ ] wallets/keys/mnemonics absent
- [ ] local databases absent
- [ ] no broad private strategy files included
- [ ] `.gitignore` blocks common runtime artifacts
- [ ] `.env.EXAMPLE` contains only empty placeholders
- [ ] scanner passes or exceptions are documented

## Common Pitfalls

1. Committing `.env.example` with real values. It should be empty placeholders only.
2. Forgetting SQLite sidecar files like `state.db-wal`.
3. Publishing profile memory or session transcripts as "examples".
4. Printing found secrets into chat/logs. Mask them.
5. Cleaning the working tree but forgetting git history if a secret was committed.
