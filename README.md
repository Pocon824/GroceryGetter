# GroceryGetter

GroceryGetter is a project aimed at tracking grocery prices over time, making shopping lists based on weekly flyers, and creating meal plans with real time inventory of your pantry.

![CI](https://github.com/Pocon824/GroceryGetter/actions/workflows/ci.yml/badge.svg)

> Work in progress.

## Stack

- **Frontend:** Angular + TypeScript (`frontend/`)
- **Backend:** Python, FastAPI, SQLite (`backend/`)
- **Extraction:** Claude API reads flyer and receipt images into structured price data
- **Tests:** pytest, Vitest (Angular), Playwright (`e2e/`)
- **CI:** GitHub Actions

## Getting started

### Backend

```powershell
cd backend
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
uvicorn app.main:app --reload
```

API docs appear at http://127.0.0.1:8000/docs.

### Frontend

```powershell
ng new frontend
cd frontend
ng serve
```

### Private data

Copy `.env.example` to `.env` and add your API key. `.env`, `data/` and everything in `inbox/` are git-ignored.

## License

MIT
