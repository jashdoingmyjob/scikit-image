# Acme Multi-Team Onboarding Runbook (Pilot -> 12 Teams)

## 1. Organization-Level Baseline (Owned by DevOps / Marcus)
- **Cursor Team Rules:** Enforce global security and secret-handling directives across all 250 seats in the Cursor Admin Dashboard.
- **Central Workflow Repo (`acme-org/engineering-workflows`):**
  - `.github/workflows/reusable-cursor-review.yml@v1`: Central CI engine (runs team repo's `check_boundaries.py` -> `pytest` -> invokes central Python orchestrator).
  - `scripts/trigger_cursor_review.py`: Central Python orchestrator that fetches live Jira acceptance criteria via OIDC/REST and invokes `POST /v1/agents` on the Cursor Cloud Agents API.

## 2. Existing Repository Onboarding (< 30 Minutes per Team)
- **Step 1 (Inner Loop):** DevOps runs the onboarding script to automatically open a "Bootstrap PR" adding `.cursor/rules/*.mdc`, `.cursor/commands/scaffold-filter.md`, and `.cursor/hooks.json`; target team Staff Eng tunes path globs and merges.
- **Step 2 (Outer Loop):** The same Bootstrap PR adds the 18-line `.github/workflows/caller-cursor-review.yml` pointer file calling `reusable-cursor-review.yml@v1`.
- **Step 3 (Branch Governance):** Apply GitHub Ruleset on `main` requiring green CI status checks, Code Owner approval, and re-approval on new pushes.
- **Step 4 (Front Door):** Register repo with Grok Bot read-only observer for QA/PM readiness summaries.