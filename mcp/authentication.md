<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/acs-cas/CAS-GraphQL-API/main/assets/logos/CAS_PREF_3C_RGB_REV.png">
  <img src="https://raw.githubusercontent.com/acs-cas/CAS-GraphQL-API/main/assets/logos/CAS_PREF_3C_RGB_POS.png" alt="CAS logo" height="64">
</picture>

# Authenticating to the CAS GraphQL MCP Server

The CAS GraphQL MCP server accepts an OAuth2 **client credentials** bearer token issued by
CAS SSO. Two steps:

1. `POST` your client ID/secret to the CAS SSO token endpoint → get an `access_token`.
2. Send that token as `Authorization: Bearer <token>` on every request to the MCP endpoint.

This is standard OAuth2.

## Endpoints

| | |
|---|---|
| Token endpoint | `https://sso.cas.org/as/token.oauth2` |
| MCP endpoint | `https://hub.cas.org/graphql/mcp` (streamable HTTP) |
| Grant type | `client_credentials` |
| Scope | `content.read` |

Credentials (`client_id` / `client_secret`) are issued by CAS Custom Services℠; obtain them
before starting. Never hard-code them — read from environment variables or a secrets store.

## Step 1 — Get a token

### curl

```bash
curl -s -X POST https://sso.cas.org/as/token.oauth2 \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=$LITHIUM_CLIENT_ID" \
  -d "client_secret=$LITHIUM_CLIENT_SECRET" \
  -d "scope=content.read"
```

Response:

```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "Bearer",
  "expires_in": 86399
}
```

Extract just the token:

```bash
TOKEN=$(curl -s -X POST https://sso.cas.org/as/token.oauth2 \
  -d grant_type=client_credentials \
  -d client_id="$LITHIUM_CLIENT_ID" \
  -d client_secret="$LITHIUM_CLIENT_SECRET" \
  -d scope=content.read | jq -r .access_token)
```

### Python

```python
import os
import httpx  # or: requests

def get_token() -> str:
    resp = httpx.post(
        "https://sso.cas.org/as/token.oauth2",
        data={
            "grant_type": "client_credentials",
            "client_id": os.environ["LITHIUM_CLIENT_ID"],
            "client_secret": os.environ["LITHIUM_CLIENT_SECRET"],
            "scope": "content.read",
        },
        timeout=30.0,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]
```

**Token lifetime:** roughly 24 hours (`expires_in`, in seconds). Cache the token and reuse it;
re-request when it is about to expire or when the MCP server returns `401`. Do not fetch a new
token per call.

## Step 2 — Call the MCP server with the token

Pass the token on **every** HTTP request to the MCP endpoint:

```
Authorization: Bearer <access_token>
```

### Python (MCP SDK)

Requires the `mcp` package (`pip install mcp httpx`).

```python
import asyncio
import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

MCP_URL = "https://hub.cas.org/graphql/mcp"

async def main() -> None:
    token = get_token()  # from Step 1

    # The Authorization header must be on the httpx client so it is sent
    # on every request the MCP transport makes.
    http_client = httpx.AsyncClient(
        headers={"Authorization": f"Bearer {token}"},
        timeout=httpx.Timeout(30.0, read=300.0),
        follow_redirects=True,
    )

    async with streamable_http_client(MCP_URL, http_client=http_client) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print([t.name for t in tools.tools])

            result = await session.call_tool(
                "search_substances", {"query": "ethanol", "limit": 3}
            )
            print(result.content[0].text)

asyncio.run(main())
```

### Available tools

| Tool | Arguments |
|---|---|
| `search_substances` | `query` (str), `limit` (int, default 10), `identifier_type` (optional) |
| `execute_graphql_query` | `query` (str) — read-only GraphQL |
| `list_query_types_tool` | none |
| `describe_type_tool` | `type_name` (str) |

## Troubleshooting

| Symptom | Cause |
|---|---|
| `401` from the token endpoint | Wrong `client_id` / `client_secret`. |
| `400 invalid_scope` | The client is not provisioned for `content.read`. |
| `401` from the MCP endpoint | Token expired (~24h) or the header is missing on a follow-up request — make sure the header is set on the HTTP client, not just the first call. |
