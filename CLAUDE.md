# Claude AI Assistant Instructions

This file contains information for Claude AI to better understand and work with this Django blog project.

## Project Overview

This is a personal Django blog website (eduzen.ar) that uses HTMX for dynamic interactions without JavaScript. The project has been recently refactored to eliminate template duplication and improve HTMX implementation.

## Key Technologies

- **Django**: Web framework
- **HTMX**: For dynamic frontend interactions
- **Alpine.js**: Minimal JavaScript for UI state management
- **Tailwind CSS**: Utility-first CSS framework
- **Docker**: Containerization
- **PostgreSQL**: Database
- **uv**: Python package manager
- **just**: Command runner (replaces make)

## Development Commands

### Environment Setup
```bash
# Copy environment file and start development
just run

# Stop the environment
just stop

# Hard stop (remove volumes)
just hard-stop

# Reset (rebuild and restart)
just reset

# View logs
just logs

# Access shell
just shell
```

### Django Management
```bash
# Check deployment readiness
just check

# Run migrations
just migrate

# Create migrations
just makemigrations

# Create superuser
just createsuperuser admin

# Show all URLs
just showurls

# Improve posts (ChatGPT integration)
just improve-posts
```

### Development Tools
```bash
# Format code (pre-commit)
just fmt

# Type checking
just mypy

# Run tests with coverage
just test

# Full coverage report
just coverage

# Build Docker image
just build
```

### Direct uv Commands
```bash
# Run Django server locally (outside Docker)
uv run python manage.py runserver

# Django shell with extensions
uv run python manage.py shell_plus

# Any Django management command
uv run python manage.py <command>
```

## Project Structure

```
website/
├── blog/                 # Main blog application
│   ├── templates/blog/   # Blog templates
│   ├── models.py         # Post, Tag models
│   ├── views.py          # Blog views
│   └── services/         # Business logic (ChatGPT, Telegram, etc.)
├── core/                 # Core utilities and base templates
│   ├── templates/core/   # Base templates, navigation, utils
│   └── static/core/      # CSS, JS, images
├── snippets/             # Code snippets feature
├── django_fast/          # Performance optimization app
├── justfile              # Command runner (preferred over Makefile)
└── Makefile             # Legacy (use justfile instead)
```

## HTMX Implementation

The website uses HTMX for SPA-like behavior. Recent refactoring (2024) eliminated template duplication:

### Template Pattern
All main templates now use this pattern:
```django
{% load django_htmx %}

{% if not request.htmx %}
{% extends 'core/utils/base.html' %}
{% block content %}
{% endif %}

<!-- Actual content here -->

{% if not request.htmx %}
{% endblock content %}
{% endif %}
```

### HTMX Features
- **Single Template Design**: Each template serves both full page and HTMX partial requests
- **Global Loading Indicators**: Centralized loading bar for all HTMX requests
- **Error Handling**: Visual feedback for failed requests (red loading bar)
- **Navigation**: All nav links use HTMX for SPA-like experience
- **Optimized Attributes**: Removed redundant `hx-trigger="click"` and `hx-swap="innerHTML"`

### HTMX Attributes Used
- `hx-get`: Load content via GET request
- `hx-target="#content"`: Target the main content area
- `hx-push-url="true"`: Update browser URL
- Global event handlers in base.html for loading states

## Common Issues & Solutions

### Template Errors
- Always use `{% load django_htmx %}` in templates that check `request.htmx`
- Ensure no duplicate partials exist (they were removed in 2024 refactor)

### HTMX Issues
- Check that `hx-target="#content"` exists in base template
- Verify global HTMX event handlers in `core/templates/core/utils/base.html`
- Navbar duplication was fixed by proper `request.htmx` detection

### Development
- Use `just fmt` before committing (runs pre-commit hooks)
- Run `just test` to ensure tests pass
- Check `just mypy` for type issues
- Use `just check` for Django deployment checks

## Testing

```bash
# Run all tests with coverage
just test

# Full coverage report
just coverage

# Run specific test
uv run python manage.py test blog.tests.test_views
```

## Deployment

The project uses Docker for deployment:

```bash
# Build production image
just build

# Check production settings
just check

# Run production-like environment
just run
```

## Recent Changes (2024)

### HTMX Refactoring
- **Eliminated Template Duplication**: Removed 7 duplicate partial templates
- **Single Template Pattern**: Templates now handle both full-page and HTMX requests
- **Global HTMX Handlers**: Added centralized loading and error handling
- **Optimized Attributes**: Removed redundant HTMX attributes
- **Fixed Navbar Duplication**: Proper content targeting prevents navbar duplication
- **Alpine.js Cleanup**: Reduced conflicts between Alpine.js and HTMX

### Key Benefits
- 50% fewer template files
- No more navbar duplication issues
- Cleaner HTMX implementation
- Better error handling and loading states
- More maintainable codebase

## Code Style

- Use pre-commit hooks (`just fmt`)
- Follow Django best practices
- Type hints with mypy
- Template naming: `_content.html` for partials included by both full and HTMX templates

## Environment Variables

Key environment variables (see `.env.sample`):
- `DATABASE_URL`: PostgreSQL connection
- `DJANGO_SETTINGS_MODULE`: Settings module
- `SECRET_KEY`: Django secret key
- API keys for ChatGPT, Telegram integration

## Useful URLs

- `/admin/`: Django admin
- `/blog/`: Blog posts list
- `/about/`: About page
- `/contact/`: Contact form
- `/consultancy/`: Consultancy services
- `/classes/`: Programming classes
- `/search/`: Search functionality

## Architecture Notes

- **Templates**: Use `{% if not request.htmx %}` pattern for dual rendering
- **Navigation**: All links use HTMX with fallback href for accessibility
- **Loading States**: Global HTMX event handlers manage loading indicators
- **Error Handling**: Failed requests show red loading bar and console errors
- **Mobile**: Alpine.js handles mobile menu state, HTMX handles navigation