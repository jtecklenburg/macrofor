**Environment & Setup**

- Purpose: reproduce a working Python environment to run the notebooks in `docs/` and the test-suite.

Runtime requirements (see `requirements.txt`):
- `sympy` (symbolic math used in notebooks)
- `numpy` (numerical arrays)
- `pillow` (image I/O for frames and GIF creation)

Development / test requirements (see `requirements-dev.txt`):
- `pytest` (run tests)
- `jupyterlab` / `nbconvert` (execute notebooks)
- `ipykernel`, `nbformat` (notebook execution)

Quick setup (PowerShell):

```powershell
# from repo root:
python -m pip install --upgrade pip
# install the package in editable mode so tests import local code
python -m pip install -e .
# install runtime deps
python -m pip install -r requirements.txt
# install dev deps
python -m pip install -r requirements-dev.txt
```

Run tests:

```powershell
# run pytest from repo root
python -m pytest -q
```

Execute a notebook (headless) and save the executed result:

```powershell
# executes notebook and writes executed notebook next to original
jupyter nbconvert --to notebook --execute docs\oregonator_operator_splitting.ipynb --ExecutePreprocessor.timeout=600 --output docs\oregonator_operator_splitting_executed.ipynb
```

Notes:
- A Fortran compiler (e.g., `gfortran`) is required only if you plan to compile the generated Fortran code from the notebooks. Install via your OS package manager (MSYS2/MinGW or WSL on Windows, brew on macOS, apt/yum on Linux).
- If you want an isolated environment, consider using `python -m venv .venv` then `.\.venv\Scripts\Activate.ps1` before installing.
