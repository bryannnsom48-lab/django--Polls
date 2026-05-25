# AI Agent Instructions for Django Polls Project

## Project Overview
- **Type**: Django web application (polls/survey system)
- **Django Version**: 6.0.2
- **Main App**: `Polls` in `PollApplication/Polls`
- **Package**: `django-Polls` (distributable package in `django-Polls/`)

## Current Scope
> **Note**: This project currently does **not** have a subscription/notification feature. The app is a simple polls system with:
> - `Question` model (poll questions)
> - `Choice` model (poll options with vote counts)
> - Voting views and results display

If adding subscription features is desired, see [docs/guides/contributing](django-Polls/docs/FAQ's/contributing.rst) for contribution guidelines.

## Essential Commands

### Development Server
```bash
# Activate virtual environment first
.\PollVenv\Scripts\Activate.ps1  # or activate.bat

# Run development server
python manage.py runserver
```

### Database
```bash
python manage.py migrate
python manage.py makemigrations Polls
python manage.py shell
```

### Testing
```bash
python manage.py test Polls
```

### Documentation (Sphinx)
```bash
cd django-Polls/docs
./make.bat html
```

## Project Structure
- `PollApplication/` - Django project settings
- `PollApplication/Polls/` - Main polls app (models, views, urls, admin)
- `django-Polls/` - Distributable package with docs
- `PollVenv/` - Virtual environment (NOT `Scripts/` at root)

## Key Files
- [manage.py](manage.py) - Django management CLI
- [PollApplication/settings.py](PollApplication/settings.py) - Django settings
- [PollApplication/Polls/models.py](PollApplication/Polls/models.py) - Data models
- [PollApplication/Polls/views.py](PollApplication/Polls/views.py) - View logic
- [django-Polls/docs/conf.py](django-Polls/docs/conf.py) - Sphinx config

## Common Patterns
- App is registered as `'Polls'` in `INSTALLED_APPS`
- URL prefix is `"Polls"` (capitalized)
- Templates in `PollApplication/Polls/templates/Polls/`
- Static files in `PollApplication/Polls/static/Polls/`

## Known Issues
- Sphinx autodoc fails if virtual environment isn't activated
- Module `django_Polls` (package) is separate from `Polls` (app)

## Documentation
- [Installation Guide](django-Polls/docs/docs/guides/installation.rst) - Setup instructions
- [Contributing FAQ](django-Polls/docs/FAQ's/contributing.rst) - Bug reporting, code submission
- [API Reference](django-Polls/docs/docs/api/index.rst) - Endpoints and views