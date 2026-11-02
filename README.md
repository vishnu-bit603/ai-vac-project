# ContentIQ — AI Content Quality and Originality Review System

Medium-level Flask application with registration/login, SQLite persistence, dashboard, review history, multi-provider AI analysis (Groq, OpenAI, Anthropic Claude), AI reply, and CSV export.

## Requirements
- Python 3.10+
- A key for at least one provider: Groq, OpenAI, or Anthropic.
- Internet access for the selected provider API and optional Google Fonts.

## Windows / VS Code setup

1. Extract the ZIP and open the extracted `AI_Content_Quality_Originality_System` folder in VS Code.
2. Open Terminal → New Terminal.
3. Create and activate a virtual environment:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\venv\Scripts\Activate.ps1
   ```

4. Install packages:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Create your private environment file:
   ```powershell
   Copy-Item .env.example .env
   ```
   Open `.env`. Paste the API key for the provider(s) you want to use. Example:
   ```env
   SECRET_KEY=use-a-long-random-secret-value
   GROQ_API_KEY=your_groq_key
   GROQ_MODEL=llama-3.3-70b-versatile
   OPENAI_API_KEY=
   OPENAI_MODEL=gpt-4o-mini
   ANTHROPIC_API_KEY=
   ANTHROPIC_MODEL=claude-3-5-haiku-latest
   ```
   You may configure one, two or all three providers. A provider is selectable only after its key is configured. The dropdown currently lists all providers; if you select one without a key, the app shows a clear configuration error.

6. Start the server:
   ```powershell
   python run.py
   ```
7. Open http://127.0.0.1:5000 in your browser.
8. Register an account, sign in, select a configured provider, paste text (40–30,000 characters), and run an analysis.

Stop Flask with Ctrl+C.

## Project structure

- `run.py`: development entry point
- `config.py`: Flask configuration
- `app/__init__.py`: app factory, extensions and database initialization
- `app/models.py`: User and Review SQLAlchemy models
- `app/auth.py`: registration, login and logout
- `app/dashboard.py`: dashboard statistics and recent reviews
- `app/analysis.py`: review submission and persistence
- `app/ai_service.py`: Groq/OpenAI/Anthropic API adapters
- `app/reports.py`: history, result detail and CSV export
- `app/templates/`: Jinja templates
- `app/static/`: CSS and JavaScript
- `instance/review.db`: created automatically on first run

## Important limitations and safety
- The originality-risk label is an AI-generated language assessment, not a search against the web or academic plagiarism databases.
- AI-style estimates are unreliable and must not be used as proof that a person used AI.
- The system does not verify citations or factual claims automatically.
- Keep API keys in `.env`; never paste them into Python, HTML, screenshots, or GitHub.
- This is a local development project. Before public deployment, set a strong SECRET_KEY, disable debug mode, add CSRF protection and rate limiting, configure HTTPS, secure cookies, backups and production database settings.
- User authentication is included for a learning/demo project. Have the security design reviewed before using with sensitive or real user data.

## Common troubleshooting

- `ModuleNotFoundError`: activate `venv` and run `pip install -r requirements.txt`.
- Missing provider key: add the matching key in `.env`, save, stop Flask with Ctrl+C, then restart `python run.py`.
- Model not available: update the corresponding `*_MODEL` setting to a model available to your provider account.
- API quota/billing errors: check the provider account and usage limits.
- Port already in use: stop the other Flask process or change the port in `run.py`.
