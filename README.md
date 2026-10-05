<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/acs-cas/CAS-GraphQL-API/main/assets/logos/CAS_PREF_3C_RGB_REV.png">
  <img src="https://raw.githubusercontent.com/acs-cas/CAS-GraphQL-API/main/assets/logos/CAS_PREF_3C_RGB_POS.png" alt="CAS logo" height="64">
</picture>

# CAS GraphQL API — Notebooks

Live, cross-linked Jupyter notebooks for the CAS GraphQL API — one notebook per topic
(Overview, Authentication, GraphiQL, and each of the 8 query domains), plus a Miscellaneous Use
Cases notebook and a worked Retrosynthesis example. Every query example is **live and
executable** against the real API, not a static transcript.

The CAS GraphQL API supports workflow integration, chemical research, machine learning, and
cheminformatics use cases. Learn more about workflow integration solutions from
__[CAS Custom Services℠](https://www.cas.org/solutions/cas-custom-services/workflow-integration)__.

## What's here

```
notebooks/    00_Overview, 01_Authentication, 02_Using_GraphiQL, one per query domain,
              plus Miscellaneous Use Cases and a Retrosynthesis worked example
common/       cas_api.py (live GraphQL client)
assets/       structure/reaction images, hazard pictograms
queries/      the same runnable .graphql example files the notebooks execute
schema/       a full reference copy of the CAS GraphQL API schema (SDL)
mcp/          authentication guide for the CAS GraphQL MCP server
```

## Installation

Requires Python 3.11+.

```powershell
git clone https://github.com/acs-cas/CAS-GraphQL-API.git
cd CAS-GraphQL-API
python -m venv venv
.\venv\Scripts\activate.ps1
pip install -r requirements.txt
```

On macOS/Linux:

```bash
git clone https://github.com/acs-cas/CAS-GraphQL-API.git
cd CAS-GraphQL-API
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Open this folder in PyCharm (or VS Code / JupyterLab) and point its Python interpreter at
`venv`. Start with `notebooks/00_Overview.ipynb` — it has a "Check your setup" cell that
confirms you can authenticate before you move on to a domain notebook. Every other notebook has
the same navigation strip at the bottom to jump between topics.

## Credentials

You'll need a **Client ID** and **Client Secret** from CAS Custom Services℠. Any notebook that
calls the live API prompts for them when you run it.

Notebooks on separate kernels each prompt on their own. To enter your credentials just once,
configure the notebooks to share a single kernel: authenticate in one, then in each of the
others change the kernel to pick the already-running session.

## Schema reference

A full copy of the CAS GraphQL API schema (SDL) is included at
[`schema/graphql-schema.graphql`](schema/graphql-schema.graphql) for reference — every type,
input, and query field in one file.

This schema can change at any time as the API evolves; every effort will be made to keep this
copy current, but it's a snapshot, not a live feed — treat it as a helpful reference rather than
the final word.

## MCP Server

If you'd rather access the API through an MCP client than raw GraphQL, see
[`mcp/authentication.md`](mcp/authentication.md) for how to authenticate to the CAS GraphQL MCP
server — a separate endpoint from the GraphQL API documented in the rest of this project, with
its own OAuth2 client-credentials flow and its own set of tools
(`search_substances`, `execute_graphql_query`, `list_query_types_tool`, `describe_type_tool`).

## License

Licensed under the [Apache License, Version 2.0](LICENSE).
