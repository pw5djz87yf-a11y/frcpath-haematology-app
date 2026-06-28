# FRCPath Haematology Revision App

A browser-based revision portal for professional haematology study.

## Launch the app

Open the [FRCPath Haematology Revision App](https://pw5djz87yf-a11y.github.io/frcpath-haematology-app/).


## Guest mode and optional cloud sync

The app works immediately without an account and saves guest progress in the browser. Optional Supabase authentication adds email/password login, magic links, cross-device progress sync, personal notes, and a protected administrator dashboard.

Supabase is deliberately unconfigured by default. See [docs/SUPABASE_SETUP.md](docs/SUPABASE_SETUP.md) for the database schema, Row Level Security policies, administrator setup, and safe public configuration values.


## Importing questions during development

Open **Question Bank → Import Questions** and choose a JSON file. The file may be a direct array of questions or an object containing a `cases` array. The app validates the structure and answer options, rejects duplicate AML codes, and stores accepted questions in that browser's local storage.

Imported questions supplement the repository banks loaded through `aml-question-bank-manifest.json`. They are local to the current browser and are not written to Supabase or committed to the repository.

## Export a test release

The **Export test release** GitHub Actions workflow creates a downloadable, self-contained ZIP containing:

- the app as `index.html`;
- a generated question-bank manifest;
- every `frcpath_gs_aml_*.json` question bank;
- release metadata and local testing instructions.

The workflow runs automatically when the app or an AML JSON bank changes. To create one on demand, open **Actions → Export test release → Run workflow**, then download the artifact from the completed run.

To build the same package locally:

```text
python scripts/export_release.py
```

The output is `build/frcpath-haematology-release.zip`. After extracting it, start a local server from the release folder:

```text
python -m http.server 8000
```

Then open `http://localhost:8000`. Opening `index.html` directly is not supported because browsers normally block local JSON requests.
