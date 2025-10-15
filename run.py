"""run.py - project-local launcher

This script ensures the project's `.venv` python is used to run `app.py`.
If the current interpreter is not the `.venv` python, this launcher will re-exec
the process using the venv python, preserving argv. If no `.venv` exists, it
prints instructions for creating one and falls back to the current interpreter.

Usage:
    python run.py           # will relaunch using .venv\Scripts\python.exe (Windows) or .venv/bin/python (POSIX)
    python run.py -- arg1   # passes args through to app.py

"""
from pathlib import Path
import os
import sys


def _ensure_and_reexec_venv(script_to_run: str):
    project_root = Path(__file__).resolve().parent
    venv_dir = project_root / ".venv"

    # If the environment already indicates a venv, do nothing
    if os.environ.get("VIRTUAL_ENV"):
        return False

    current_exe = Path(sys.executable).resolve()

    # Candidate venv python paths (Windows and POSIX)
    candidates = []
    if sys.platform == "win32":
        candidates.append(venv_dir / "Scripts" / "python.exe")
        candidates.append(venv_dir / "Scripts" / "python")
    else:
        candidates.append(venv_dir / "bin" / "python")

    for candidate in candidates:
        try:
            candidate = candidate.resolve()
        except Exception:
            continue
        if not candidate.exists():
            continue

        # If we're already running that python, set VIRTUAL_ENV and continue
        if candidate == current_exe:
            os.environ["VIRTUAL_ENV"] = str(venv_dir)
            return False

        # Re-exec the script under the venv python
        args = [str(candidate), script_to_run] + sys.argv[1:]
        print(f"Re-launching using virtual environment python: {candidate}")
        try:
            os.execv(str(candidate), args)
        except Exception as e:
            print(f"Failed to re-exec with {candidate}: {e}")
            return False

    # No venv python found — print instructions to create one
    print("Virtual environment not found at '.venv'. To create one, run:")
    print()
    print("python -m venv .venv")
    print(".venv\\Scripts\\python.exe run.py  # Windows")
    print(".venv/bin/python run.py  # macOS/Linux")
    print()
    return False


if __name__ == "__main__":
    # Determine the script to run (app.py) located in the same project root
    script_path = Path(__file__).resolve().parent / "app.py"
    if not script_path.exists():
        print(f"Expected {script_path} to exist. Nothing to run.")
        sys.exit(1)

    # Attempt to ensure venv and re-exec if needed
    _ensure_and_reexec_venv(str(script_path))

    # If we reach here, either we're already on the venv python or no venv exists
    # Execute app.py in the current interpreter
    with open(script_path, "r", encoding="utf-8") as f:
        source = f.read()
    # Execute in a fresh globals dict to mimic running as a script
    globals_dict = {"__name__": "__main__", "__file__": str(script_path)}
    exec(compile(source, str(script_path), "exec"), globals_dict)
