# FRCPath Haematology Revision App

A browser-based revision portal for professional haematology study.

## Launch the app

Open the [FRCPath Haematology Revision App](https://pw5djz87yf-a11y.github.io/frcpath-haematology-app/).

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
