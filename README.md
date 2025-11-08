# FastAPI + Python 3.14 — Quick Install

## Requirements

- Python 3.14 (or system Python named `python3.14`)
- pip

## Install Python 3.14 (recommended via pyenv)

```bash
# Install pyenv first (macOS / Linux)
curl https://pyenv.run | bash
# then
pyenv install 3.14.0
pyenv virtualenv 3.14.0 venv-3.14
pyenv activate venv-3.14
```

(Or use your OS package manager / installer to get python3.14.)

## Create virtualenv and install FastAPI + Uvicorn

```bash
python3.14 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn[standard]
```

## Minimal app

Create `app/main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
  return {"message": "Hello, FastAPI + Python 3.14"}
```

## Run with Uvicorn

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://127.0.0.1:8000/ and docs at http://127.0.0.1:8000/docs
