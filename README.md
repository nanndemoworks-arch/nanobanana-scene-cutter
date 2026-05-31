# Nanobanana Scene Cutter

`Nanobanana Scene Cutter` is an open-source Streamlit app that turns a single source image into a 3x3 cinematic contact sheet with nine distinct shot types. It is designed for creators who want to explore AI-assisted storyboard generation, shot planning, and scene variation from one input frame.

## Why this project exists

Many image-generation tools can make a single strong frame, but they do not help much with shot coverage. This project focuses on a practical production problem: generating consistent wide, medium, close, low-angle, and high-angle variations from the same scene so creators can move faster from concept image to storyboard.

## Core features

- Generate a 3x3 cinematic contact sheet from one uploaded image
- Keep subject, lighting, and environment as consistent as possible across all nine cuts
- Select only the useful cuts and export them as a ZIP archive
- Optionally upscale selected cuts before download
- Run locally with a lightweight Streamlit interface

## Shot coverage

The app generates these nine views:

1. Extreme Long Shot
2. Long Shot
3. Medium Long Shot / 3/4
4. Medium Shot
5. Medium Close-Up
6. Close-Up
7. Extreme Close-Up
8. Low Angle Shot
9. High Angle Shot

## Project status

Status: active early-stage project

Current maintenance focus:

- improve prompt consistency across different source images
- make output selection and export more reliable
- document setup and contribution flow clearly
- add basic CI and issue triage structure for external contributors

## Tech stack

- Python 3.10+
- Streamlit
- fal.ai / `fal-client`
- Pillow
- Requests

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/nanndemoworks-arch/nanobanana-scene-cutter.git
cd nanobanana-scene-cutter
```

### 2. Create a virtual environment

```bash
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

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

Then open `http://localhost:8501`.

## Usage

1. Launch the app locally.
2. Enter your `fal.ai` API key in the sidebar.
3. Upload a source image.
4. Generate the 3x3 contact sheet.
5. Review the nine cuts.
6. Select the useful cuts and download them as ZIP.

## API cost note

This repository is open source, but image generation itself uses the `fal.ai` API. That means:

- the code in this repository can be used, modified, and contributed to under the repository license
- generation and upscaling requests can still incur third-party API charges

Check current pricing and usage limits on the `fal.ai` side before heavy use.

## Development notes

This app is intentionally small and easy to inspect. The current structure is:

- `app.py`: Streamlit UI and generation workflow
- `requirements.txt`: runtime dependencies
- `CONTRIBUTING.md`: contribution guidance

## Roadmap

- add reproducible example inputs and outputs
- improve prompt controls for style and framing stability
- support batch processing for multiple source images
- add tests for utility paths that do not require API calls
- improve deployment options for hosted demo environments

## Contributing

Contributions are welcome, especially in these areas:

- bug fixes around upload, crop, and export flows
- prompt tuning for better multi-shot consistency
- UI improvements for review and selection
- documentation and reproducibility improvements

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the expected workflow.

## Reporting issues

Please use GitHub Issues for:

- bug reports
- feature requests
- setup problems
- ideas for workflow improvements

Issue and pull request templates are included in `.github/`.

## License

This project is released under the [MIT License](./LICENSE).
