# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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

# Run tests
uv run pytest

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
Templates now use django-template-partials for cleaner HTMX integration:

**View Pattern:**
```python
class MyView(TemplateView):
    template_name = "app/template.html"

    def get_template_names(self):
        if self.request.htmx:
            return ["app/template.html#partial-name"]
        return [self.template_name]
```

**Template Pattern:**
```django
{% extends 'core/utils/base.html' %}
{% load partials %}

{% block content %}

{% partialdef partial-name %}
<!-- Actual content here -->
{% endpartialdef partial-name %}

{% partial partial-name %}

{% endblock content %}
```

**Important**:
- Do NOT use `request.htmx` checks in templates. Use django-template-partials instead.
- Use `{% static %}` instead of `{% get_static_prefix %}` within partialdef blocks.

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
- Always use `{% load partials %}` for django-template-partials
- Do NOT use `request.htmx` checks - use partialdef instead
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

## Testing

The project has comprehensive test coverage with pytest:

```bash
# Run all tests with coverage
just test

# Full coverage report
just coverage

# Run specific test file
uv run pytest blog/tests/views/test_home_view.py

# Run specific test class
uv run pytest blog/tests/views/test_home_view.py::TestHomeView

# Run with parallel execution
uv run pytest -n auto
```

### E2E Testing with Playwright

The project supports end-to-end testing with Playwright. Dependencies are separated into an `e2e` group for granular installations:

```bash
# Run E2E tests (development environment)
just e2e
just e2e-headed  # With browser UI
just e2e-debug   # Slow motion debugging
```

**Docker E2E Layer**: The Dockerfile includes a dedicated `e2e` stage with:
- Playwright browsers pre-installed
- Additional system dependencies for browser compatibility
- Proper Docker flags (`--init`, `--ipc=host`) following Playwright best practices

### Test Structure
- **Unit Tests**: Located in `*/tests/` directories
- **View Tests**: Comprehensive testing of all views with HTMX support
- **Service Tests**: Testing business logic (ChatGPT, Telegram, etc.)
- **Factory Tests**: Using factory-boy for test data generation
- **E2E Tests**: End-to-end browser tests with Playwright
- **Coverage**: Minimum 80% coverage required

## Recent Changes (2024)

### Django-Template-Partials Migration (Latest)
- **Converted All Views**: Migrated from `HtmxGetMixin` to django-template-partials pattern
- **Template Consolidation**: All 8 views now use single-template structure with `{% partialdef %}`
- **View Pattern**: Views use `get_template_names()` returning `"template.html#partial-name"` for HTMX requests
- **File Cleanup**: Removed 8 unused `_*.html` partial template files
- **Static File Fix**: Fixed image 404s by replacing `{% get_static_prefix %}` with `{% static %}` in partials
- **Alpine.js Improvements**: Enhanced image slideshow with pause-on-hover and proper memory management

### HTMX Refactoring
- **Eliminated Template Duplication**: Removed 7 duplicate partial templates
- **Single Template Pattern**: Templates now handle both full-page and HTMX requests
- **Global HTMX Handlers**: Added centralized loading and error handling
- **Optimized Attributes**: Removed redundant HTMX attributes
- **Fixed Navbar Duplication**: Proper content targeting prevents navbar duplication
- **Alpine.js Cleanup**: Reduced conflicts between Alpine.js and HTMX

### Key Benefits
- 50% fewer template files (eliminated all `_*.html` partials)
- No more navbar duplication issues
- Cleaner HTMX implementation with django-template-partials
- Better error handling and loading states
- More maintainable codebase with single-template architecture
- Proper static file handling in partial contexts

## Code Style

- Use pre-commit hooks (`just fmt`)
- Follow Django best practices
- Type hints with mypy
- Python 3.13+ with modern syntax
- Ruff for linting and formatting
- Coverage minimum 80%

## Environment Variables

Key environment variables (see `.env.sample`):
- `DATABASE_URL`: PostgreSQL connection
- `DJANGO_SETTINGS_MODULE`: Settings module
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (False in production)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
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

### Core Architecture
- **Django Apps**: `blog` (main content), `core` (utilities), `snippets` (code snippets), `django_fast` (performance)
- **Templates**: Use django-template-partials with `{% partialdef %}` for dual rendering
- **Navigation**: All links use HTMX with fallback href for accessibility
- **Loading States**: Global HTMX event handlers manage loading indicators
- **Error Handling**: Failed requests show red loading bar and console errors
- **Mobile**: Alpine.js handles mobile menu state, HTMX handles navigation

### Key Patterns
- **Service Layer**: Business logic in `*/services/` modules (ChatGPT, Telegram, etc.)
- **Factory Pattern**: Test data generation with factory-boy
- **Type Safety**: Full type hints with mypy and django-stubs
- **Caching**: Custom caching service in `django_fast` app
- **Internationalization**: Django i18n with English/Spanish support

### Performance Optimizations
- **Static Files**: Whitenoise with Brotli compression
- **Database**: PostgreSQL with connection pooling
- **Caching**: Redis for session/cache backend
- **Monitoring**: Logfire integration for observability
- **CDN**: Static file serving optimized for production

- Use always justfile recipes
