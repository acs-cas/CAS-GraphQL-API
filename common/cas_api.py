"""Shared live client for the CAS GraphQL API.

Credentials are entered interactively via input()/getpass() -- never hard-coded
in a cell -- so there is nothing to "blank out" before pushing a notebook to
GitHub. The client secret is masked as you type. A cell's *output* can still
end up in the .ipynb file once you run it, so before publishing run
Kernel > Restart Kernel and Clear All Outputs (or `jupyter nbconvert --clear-output`)
to drop any cached responses/tokens from the saved file.

See notebooks/01_Authentication.ipynb for the manual, unwrapped version of this
same flow -- this module exists so the domain notebooks (03+) don't have to
repeat it in every notebook.
"""
from __future__ import annotations

import getpass
import time

import requests

TOKEN_URL = "https://sso.cas.org/as/token.oauth2"
GRAPHQL_URL = "https://lithium.cas.org/graphql"
SCOPE = "content.read"

_credentials: tuple[str, str] | None = None
_token: str | None = None
_token_expires_at: float = 0.0


def _prompt_credentials() -> tuple[str, str]:
    global _credentials
    if _credentials is None:
        client_id = input("CAS Client ID: ").strip()
        client_secret = getpass.getpass("CAS Client Secret (input hidden): ").strip()
        _credentials = (client_id, client_secret)
    return _credentials


def get_access_token(force_refresh: bool = False) -> str:
    """Return a cached bearer token, requesting a new one if missing/expired.

    Prompts for credentials on first use (this session only -- nothing is
    written to disk). Reused automatically by graphql() below.
    """
    global _token, _token_expires_at

    if not force_refresh and _token and time.time() < _token_expires_at:
        return _token

    client_id, client_secret = _prompt_credentials()
    response = requests.post(
        TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": SCOPE,
        },
        timeout=30,
    )
    if not response.ok:
        try:
            detail = response.json().get("error_description", response.text)
        except ValueError:
            detail = response.text
        _credentials = None  # let the next call re-prompt rather than retry bad creds silently
        raise RuntimeError(f"Token request failed ({response.status_code}): {detail}")
    payload = response.json()

    _token = payload["access_token"]
    # Refresh a minute early rather than cutting it exactly at expiry.
    _token_expires_at = time.time() + payload.get("expires_in", 86399) - 60
    print(f"Access token acquired (expires in {payload.get('expires_in', 86399)}s). "
          f"Token value is not printed here -- see the note at the top of this module.")
    return _token


def graphql(query: str, variables: dict | None = None) -> dict:
    """Run one GraphQL query against the live CAS GraphQL API and return the
    parsed JSON response (including a top-level "errors" list, if any --
    this does not raise on GraphQL-level errors, only on transport failures)."""
    token = get_access_token()
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables or {}},
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        timeout=60,
    )
    if response.status_code == 401:
        # Token likely expired mid-session -- refresh once and retry.
        token = get_access_token(force_refresh=True)
        response = requests.post(
            GRAPHQL_URL,
            json={"query": query, "variables": variables or {}},
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            timeout=60,
        )
    response.raise_for_status()
    return response.json()
