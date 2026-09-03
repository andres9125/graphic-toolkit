# Contributing

Thanks for contributing to Graphic Toolkit.

## Development setup

Create an isolated environment, install the project, and run the checks:

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
python -m unittest discover -s tests -v
python -m compileall -q src
~~~

## Contribution guidelines

- Keep commands deterministic unless a command explicitly calls an external
  service.
- Do not commit generated image assets, API keys, customer material, or
  absolute local paths.
- Add or update tests for behavior changes.
- Use a pull request and keep each change narrowly scoped.

By submitting a contribution, you agree to license it under Apache-2.0.

