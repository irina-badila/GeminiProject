# Copilot instructions for GeminiProject

Purpose: help AI coding agents be immediately productive in this repository by documenting the small project's structure, runtime workflow, and code patterns that appear in source files.

Quick facts
- Language: Python 3.14+ (see `pyproject.toml` require-python).
- Repo is minimal: top-level scripts `app.py` and `main.py`, with `README.md` describing project.

What this project does (from files)
- `app.py` is a small demo that calls Google's Generative AI SDK (`google.generativeai`) and expects a `GOOGLE_API_KEY` from environment variables (loaded via `dotenv`). It constructs a `genai.GenerativeModel('gemini-2.5-flash')` and calls `generate_content(prompt)`.
- `main.py` exposes a tiny CLI entrypoint that prints a greeting.

Key files to read first
- `app.py` — shows auth, prompt flow, and model usage patterns.
- `main.py` — minimal entrypoint; used for local script runs.
- `pyproject.toml` — project metadata; confirms Python version and that dependencies are currently empty.
- `README.md` — single-line README describing project name.

Project-specific guidance for AI agents
- Secrets and env: `app.py` expects `GOOGLE_API_KEY` to be provided via environment variables and uses `dotenv.load_dotenv()` to load from a `.env` file. When writing or modifying code that reads secrets, follow this same pattern and avoid hard-coding keys in source.
- Model API usage: follow the pattern in `app.py` — instantiate `genai.GenerativeModel('<model-name>')`, prepare a `prompt` string, and call `generate_content(prompt)`. Return types: `response.text` is used to access generated text; preserve this usage unless adding explicit error handling.
- Minimal dependencies: `pyproject.toml` lists no dependencies. If you add packages, update `pyproject.toml` accordingly and prefer the [PEP 621] style used here.
- Python version: code targets Python 3.14+; avoid using syntax that is newer than 3.14.

Typical developer workflows (discovered)
- Create and activate virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
# If execution policy blocks Activate.ps1 (common on Windows), run in PowerShell as admin or use the alternative activation command for cmd:
.\.venv\Scripts\Activate.ps1  # PowerShell (may be blocked by ExecutionPolicy)
# Alternative (PowerShell): use the cmd activation wrapper
.\.venv\Scripts\activate.bat   # runs in current shell via cmd compatibility
# Or run Python directly without activating venv:
.venv\Scripts\python.exe app.py
```

- Note: users on Windows sometimes see "running scripts is disabled" when running `Activate.ps1`. The safe local workaround for agents or CI is to use the venv python executable directly (`.venv\Scripts\python.exe`) or instruct the user to set an appropriate execution policy only if they understand the security implications.

Testing and building
- There are no tests or build steps discovered. Keep changes limited and include unit tests if adding logic. Use standard `pytest` if introducing tests and add it to `pyproject.toml`.

Conventions and patterns
- Single-file scripts: project uses simple top-level scripts with small functions. Keep changes small and explicit.
- Environment loading: `dotenv` usage is the canonical pattern for this repo.
- Logging and output: `print()` is used for console output. If adding logging, add a basic `logging` configuration at module import time.

Examples to copy from repository
- API call pattern (from `app.py`):

```python
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content('...')
print(response.text)
```

What NOT to assume
- No CI or tests: there are no CI config files or test runners present.
- No pinned dependencies: adding new packages requires updating `pyproject.toml`.

If you make changes
- Update `pyproject.toml` when adding dependencies.
- Add a short note to `README.md` when changing runtime behavior (new env vars, new commands).
- Add unit tests and a minimal `tests/` folder when modifying logic.

Where to ask for help
- If uncertain about intent behind `app.py`'s prompt flow or model choice, open an issue or PR asking the repo owner for the expected production model and env handling.

If anything here looks wrong or incomplete, tell me which area (auth, run steps, dependencies, tests) and I'll update the file.