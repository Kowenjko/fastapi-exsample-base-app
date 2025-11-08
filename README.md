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

# FastAPI Example App

```shell
gunicorn main:main_app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Resources:

- `.gitignore` for Python https://github.com/github/gitignore/blob/main/Python.gitignore
- FastAPI events https://fastapi.tiangolo.com/advanced/events/
- FastAPI lifespan events https://fastapi.tiangolo.com/advanced/events/#lifespan-function
- SQLAlchemy create engine https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine
- Python typing https://docs.python.org/3/library/typing.html
- pydantic settings dotenv https://docs.pydantic.dev/latest/concepts/pydantic_settings/#dotenv-env-support
- pydantic settings env variables https://docs.pydantic.dev/latest/concepts/pydantic_settings/#parsing-environment-variable-values
- case converter https://github.com/mahenzon/ri-sdk-python-wrapper/blob/master/ri_sdk_codegen/utils/case_converter.py
- SQLAlchemy constraint naming conventions https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions
- Alembic cookbook https://alembic.sqlalchemy.org/en/latest/cookbook.html
- Alembic naming conventions https://alembic.sqlalchemy.org/en/latest/naming.html#integration-of-naming-conventions-into-operations-autogenerate
- Alembic + asyncio recipe https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic
- orjson https://github.com/ijl/orjson
- FastAPI ORJSONResponse https://fastapi.tiangolo.com/advanced/custom-response/#use-orjsonresponse

```shell
taskiq worker core:broker --fs-discover --tasks-pattern "**/tasks"
taskiq worker core:broker --workers 1 --no-configure-logging --fs-discover --tasks-pattern "**/tasks"
```

### FastStream

```shell
faststream run fs_subs.app:app
faststream docs serve fs_subs.app:app --port 8081
```
