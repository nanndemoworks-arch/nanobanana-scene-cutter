# Contributing

Thanks for contributing to `nanobanana-scene-cutter`.

This project is still small, so the main goal is to keep contributions easy to review and easy to maintain.

## Good first contributions

- fix bugs in upload, crop, ZIP export, or upscale flows
- improve setup instructions and error messages
- tighten prompt behavior for better shot consistency
- add small testable utility functions or refactors
- improve Windows and cross-platform developer experience

## Development setup

```bash
git clone https://github.com/nanndemoworks-arch/nanobanana-scene-cutter.git
cd nanobanana-scene-cutter
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app locally:

```bash
streamlit run app.py
```

## Before opening a pull request

- keep the change focused
- update `README.md` when behavior or setup changes
- do not commit API keys, secrets, or personal assets
- make sure the app still starts cleanly
- describe user-facing impact in the pull request body

## Pull request expectations

Please include:

- what changed
- why it changed
- how to test it
- screenshots or short recordings for UI changes when possible

## Issues

Use GitHub Issues for:

- bug reports
- feature requests
- reproducible setup problems

If you are filing a bug, include the source image type, expected behavior, actual behavior, and any traceback or screenshot you have.

## Scope guidance

This repository is for the open-source app itself. Please avoid pull requests that:

- add paid service credentials
- commit generated binaries or private datasets
- bundle unrelated portfolio or agency site code

## Code style

- follow normal Python readability conventions
- prefer simple functions over clever abstractions
- keep Streamlit UI changes explicit and easy to trace
- add comments only where behavior is non-obvious

## Questions

If you are unsure whether a change fits, open an issue first and outline the use case.

