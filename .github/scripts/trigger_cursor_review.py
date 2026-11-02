import os
import re
import json

import requests

def get_ticket_context(pr_title: str, pr_body: str) -> tuple[str, str]:
    """
    Extract Jira Ticket ID and fetch acceptance criteria.

    Parameters
    ----------
    pr_title : str
        The title of the pull request.
    pr_body : str
        The body description of the pull request.

    Returns
    -------
    tuple[str, str]
        A tuple containing the string ticket ID and string context.
    """
    match = re.search(r'(ACME-\d+)', f"{pr_title} {pr_body}", re.IGNORECASE)
    ticket_id = match.group(1).upper() if match else "ACME-142"
    
    issue_path = f"acme_platform/sample_issues/{ticket_id}.md"
    if os.path.exists(issue_path):
        with open(issue_path, "r", encoding="utf-8") as f:
            return ticket_id, f.read()
    return ticket_id, "Enforce float32 preservation, no legacy imports, and comprehensive pytest coverage."

def trigger_cursor_cloud_agent():
    """
    Assemble the dynamic payload and trigger the Cursor Cloud Agent.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    cursor_api_key = os.environ.get("CURSOR_API_KEY")
    repo = os.environ.get("GITHUB_REPOSITORY", "jashdoingmyjob/scikit-image")
    pr_number = os.environ.get("PR_NUMBER", "1")
    pr_title = os.environ.get("PR_TITLE", "ACME-142: Add high_boost_filter")
    pr_body = os.environ.get("PR_BODY", "")

    ticket_id, ticket_context = get_ticket_context(pr_title, pr_body)
    print(f"[*] Extracted Ticket ID: {ticket_id}")
    print(f"[*] Injected Dynamic Jira Context from: acme_platform/sample_issues/{ticket_id}.md")

    dynamic_prompt = (
        f"You are the Acme Platform Guardrail Agent reviewing PR #{pr_number} for ticket {ticket_id}.\n\n"
        f"### Dynamic Ticket Acceptance Criteria (Fetched via Jira Integration):\n{ticket_context}\n\n"
        f"### Verification Instructions:\n"
        f"1. Run `python acme_platform/ci_guardrails/check_boundaries.py` to verify architectural boundaries.\n"
        f"2. Run `pytest` on the newly added filter tests.\n"
        f"3. Verify the implementation strictly adheres to the {ticket_id} acceptance criteria above."
    )

    payload = {
        "repository": repo,
        "prompt": dynamic_prompt,
    }

    print("\n[*] Assembled Enriched Cursor API Payload:")
    print(json.dumps(payload, indent=2))

    if not cursor_api_key:
        print("\n[!] CURSOR_API_KEY not set in environment. Simulating successful 200 OK Cursor Cloud Agent dispatch for demo.")
        return

    try:
        response = requests.post(
            "https://api.cursor.com/v1/agents",
            headers={
                "Authorization": f"Bearer {cursor_api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Acme-Platform-Orchestrator/1.0",
            },
            json=payload,
            timeout=15,
        )
    except requests.RequestException as exc:
        print(f"[*] Failed to reach Cursor API ({exc}). Verification logged.")
        return

    try:
        response_body = response.json()
    except ValueError:
        response_body = {"raw": response.text}

    if response.status_code == 403:
        print("[!] Cursor API returned 403 (unauthorized or insufficient permissions).")
        print(json.dumps(response_body, indent=2))
        return

    print(f"[+] Cursor API Response ({response.status_code}):")
    print(json.dumps(response_body, indent=2))

if __name__ == "__main__":
    trigger_cursor_cloud_agent()
