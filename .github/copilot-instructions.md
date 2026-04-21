# Project Guidelines

## Architecture

This is a simple FastAPI-based web application for Mergington High School extracurricular activities signup.

- **Backend**: FastAPI REST API with in-memory data storage (resets on restart)
- **Frontend**: Static HTML/JS/CSS served via FastAPI's StaticFiles mount
- **Data Model**: Activities keyed by name, with participants list; students identified by email

Key components:
- `src/app.py`: Core API with routing and data logic
- `src/static/index.html`: Single-page app with dynamic activity loading
- `src/static/app.js`: Frontend API calls and DOM manipulation
- `src/static/styles.css`: Basic styling

API Endpoints:
- `GET /activities`: Returns all activity data
- `POST /activities/{activity_name}/signup`: Signs up student (appends email to participants)

## Build and Test

Agents will automatically run these commands:

- Install dependencies: `pip install -r requirements.txt`
- Run development server: `python src/app.py` (starts on port 8000)
- Alternative: `uvicorn src.app:app --reload --reload-include src/static/*`
- Test: `pytest` (framework configured, but no tests exist yet)

## Conventions

- **Python path**: pytest.ini sets `pythonpath = .` for testing
- **Activity naming**: Human-readable names as primary keys (e.g., "Chess Club")
- **Email format**: Student emails use `@mergington.edu` domain
- **Data storage**: Plain Python dicts/lists, no database integration
- **Static assets**: Mounted at `/static`, root redirects to `index.html`

## Pitfalls

- **Data persistence**: All changes lost on server restart (in-memory only)
- **Validation gaps**: No duplicate signup prevention, no max participant enforcement, no email validation
- **Concurrency**: Global activities dict not thread-safe for concurrent requests
- **Dependencies**: httpx and watchfiles in requirements.txt but unused in current code
- **Testing**: No existing tests; pytest configured but no test files

For detailed API documentation, see [src/README.md](src/README.md). For exercise instructions, see [.github/steps/](.github/steps/).</content>
<parameter name="filePath">/workspaces/skills-getting-started-with-github-copilot3/.github/copilot-instructions.md