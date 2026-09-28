<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/acs-cas/CAS-GraphQL-API/main/assets/logos/CAS_PREF_3C_RGB_REV.png">
  <img src="https://raw.githubusercontent.com/acs-cas/CAS-GraphQL-API/main/assets/logos/CAS_PREF_3C_RGB_POS.png" alt="CAS logo" height="64">
</picture>

# CAS GraphQL API — Notebooks

Live, cross-linked Jupyter notebooks for the CAS GraphQL API — one notebook per topic
(Overview, Authentication, GraphiQL, and each of the 8 query domains). Every query example is
**live and executable** against the real API, not a static transcript.

The CAS GraphQL API supports workflow integration, chemical research, machine learning, and
cheminformatics use cases. Learn more about workflow integration solutions from
__[CAS Custom Services℠](https://www.cas.org/solutions/cas-custom-services/workflow-integration)__.

## What's here

```
notebooks/    00_Overview, 01_Authentication, 02_Using_GraphiQL, then one per query domain
common/       cas_api.py (live GraphQL client)
assets/       structure/reaction images, hazard pictograms
queries/      the same runnable .graphql example files the notebooks execute
```

## Installation

Requires Python 3.11+. From this directory:

```powershell
python -m venv venv
.\venv\Scripts\activate.ps1
pip install -r requirements.txt
```

On macOS/Linux:

```bash
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

You'll need a **Client ID** and **Client Secret** from CAS Custom Services℠. Every notebook
that calls the live API prompts for these interactively (`input()` for the Client ID,
`getpass()` — masked — for the secret) via `common/cas_api.py`. **Nothing is hard-coded and
nothing is written to disk**, so there's no secret sitting in the notebook source to remember to
delete before committing.

**Before re-committing a run**, the one thing to actually clear is *cell output* — once you run a
notebook, its saved file includes whatever got printed (query results, mainly; the token value
itself is deliberately never printed). Clear it with either:

- In the notebook UI: **Kernel > Restart Kernel and Clear All Outputs**, then save, or
- From the command line: `jupyter nbconvert --clear-output --inplace notebooks/*.ipynb`

## License

Licensed under the [Apache License, Version 2.0](LICENSE).
