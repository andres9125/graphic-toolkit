# Graphic Toolkit

[![Validation](https://github.com/andres9125/graphic-toolkit/actions/workflows/validation.yml/badge.svg)](https://github.com/andres9125/graphic-toolkit/actions/workflows/validation.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

Graphic Toolkit is a small Python command-line utility for producing
reproducible web and social-media assets from one raster source image. It is
useful when a project needs consistent favicon files, app icons, square brand
images, or a social sharing card without an ad-hoc export script.

It operates locally by default. The optional `openai-generate` command sends a
prompt to the OpenAI Images API only when you invoke it and provide your own
`OPENAI_API_KEY`.

## Capabilities

| Command | Input | Output |
| --- | --- | --- |
| `favicon-pack` | One raster image | PNG favicon variants, Apple touch icon, multi-size ICO, and a manifest. |
| `brand-pack` | One raster image | 1024px and 512px PNGs, a transparent preview, a 1200x630 social card, and a manifest. |
| `openai-generate` | A text prompt and an API key | A PNG returned by the OpenAI Images API plus a privacy-conscious manifest. |

The local commands accept formats supported by Pillow, including PNG, JPEG,
and WebP. SVG is deliberately not supported in this release, so the package
does not depend on an SVG renderer with a copyleft license.

## Install

Python 3.10 or later is required.

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
~~~

## Usage

Create a favicon pack:

~~~powershell
graphic-toolkit favicon-pack .\logo.png --out .\artifacts\favicon
~~~

Create a brand and social pack with a custom background for JPEG output:

~~~powershell
graphic-toolkit brand-pack .\logo.png --out .\artifacts\brand --background "#0B1020"
~~~

Generate an image through OpenAI. This command makes a billable network request
and requires an API key in the environment:

~~~powershell
$env:OPENAI_API_KEY = "your-api-key"
graphic-toolkit openai-generate "A geometric cloud icon on a transparent background" --out .\artifacts\generated
~~~

Use `graphic-toolkit <command> --help` to see padding, output, size, quality,
and model options. The OpenAI command defaults to `gpt-image-2`; you can
provide a supported model explicitly with `--model`.

## Output and privacy

Each command writes a `manifest.json` next to its generated files. Manifests
record output file names and non-sensitive processing options. They do not
record absolute source paths, API keys, or the full AI prompt.

Do not pass confidential information in an AI prompt. Review OpenAI's
[image generation documentation](https://developers.openai.com/api/docs/models)
and applicable policies before using the optional network command.

## Limits

- This is an asset-export helper, not a Figma, Illustrator, or vector-editing
  replacement.
- It does not edit SVG files or preserve a vector workflow.
- It does not validate trademark ownership or brand guidelines; you are
  responsible for the source assets and generated content you use.
- The OpenAI command requires network access and a separately configured API
  account. All other commands work offline.

## Development

~~~powershell
python -m unittest discover -s tests -v
python -m compileall -q src
~~~

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md) before
opening a pull request.

## License

Copyright 2026 Eximus. Licensed under [Apache-2.0](LICENSE). See
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for dependency notices.

