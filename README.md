# My Django Blog: [eduzen.ar](http://eduzen.ar)

Welcome to my personal Django blog powered by HTMX, a modern approach to full-stack development. This project is a blend of several technologies that aim to create a seamless blogging experience with SPA-like behavior without JavaScript frameworks.

![Python application](https://github.com/eduzen/website/workflows/Python%20application/badge.svg)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

## Features

- **Django Backend**: The power of Django for the backend ensures stability and scalability.
- **HTMX Integration**: Seamless SPA-like experience without JavaScript frameworks. Recently refactored (2024) for optimal performance:
  - Eliminated template duplication (50% fewer template files)
  - Single templates handle both full-page and HTMX partial requests
  - Global loading indicators and error handling
  - Fixed navbar duplication issues
- **Alpine.js**: Minimal JavaScript for UI state management (mobile menu, image carousels)
- **Tailwind CSS**: Utility-first CSS framework for rapid UI development
- **ChatGPT API**: Using the ChatGPT API for dynamic content creation and engagement
- **GitHub Actions**: Continuous integration ensuring code quality and automatic deployments
- **Dockerized**: The entire setup is containerized using Docker for consistent development and deployment
- **Static Typing with Mypy**: Bringing the power of static typing to Python
- **uv**: Fast Python package manager and project management
- **Pre-commit**: Automated checks before commits to ensure code quality
- **just**: Modern command runner replacing traditional Makefiles

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:
- Docker and Docker Compose
- [just](https://github.com/casey/just) command runner (optional, but recommended)
- [uv](https://github.com/astral-sh/uv) for local Python development (optional)

### Quick Start

1. **Clone and Start**:
   ```bash
   git clone https://github.com/eduzen/website.git
   cd website
   just run  # This copies .env.sample to .env and starts the application
   ```

2. **Run Migrations**:
   ```bash
   just migrate
   ```

3. **Create Superuser**:
   ```bash
   just createsuperuser admin
   ```

### Development Commands

```bash
# Start development environment
just run

# Stop the application
just stop

# View logs
just logs

# Access shell
just shell

# Run tests
just test

# Format code
just fmt

# Type checking
just mypy

# Check deployment readiness
just check
```

### Local Development (without Docker)

If you have `uv` installed, you can run the project locally:

```bash
# Install dependencies
uv sync

# Run migrations
uv run python manage.py migrate

# Start development server
uv run python manage.py runserver
```

## Recent Improvements (2024)

### HTMX Refactoring

The website underwent a major HTMX refactoring to improve maintainability and fix issues:

**Problems Solved:**
- ❌ Template duplication (7 duplicate partial templates)
- ❌ Navbar duplication issues
- ❌ Redundant HTMX attributes
- ❌ Conflicts between Alpine.js and HTMX

**Solutions Implemented:**
- ✅ **Single Template Pattern**: Each template now handles both full-page and HTMX partial requests using `{% if not request.htmx %}`
- ✅ **Global HTMX Handlers**: Centralized loading indicators and error handling
- ✅ **Optimized Attributes**: Removed redundant `hx-trigger="click"` and `hx-swap="innerHTML"`
- ✅ **Fixed Navbar Duplication**: Proper content targeting prevents navbar from appearing in HTMX responses
- ✅ **Cleaner Alpine.js Integration**: Reduced conflicts and improved mobile menu handling

**Results:**
- 50% fewer template files
- No more navbar duplication
- Better error handling with visual feedback
- Cleaner, more maintainable codebase

## Architecture

### HTMX Implementation

The website provides a SPA-like experience using HTMX:

- **Navigation**: All nav links use HTMX for seamless page transitions
- **Content Loading**: Dynamic content loading without page refreshes
- **Loading States**: Global loading indicator with error handling
- **Fallback Support**: All HTMX links include `href` attributes for accessibility
- **Mobile Friendly**: Alpine.js handles mobile menu state

### Template Structure

```
core/templates/core/utils/
├── base.html          # Main layout with HTMX event handlers
├── navbar.html        # Navigation with HTMX links
├── nav_links.html     # Desktop navigation links
├── nav_links_mobile.html # Mobile navigation links
└── partial.html       # Minimal template for HTMX responses

blog/templates/blog/
├── home.html          # Homepage (full + HTMX)
├── about.html         # About page (full + HTMX)
├── _about.html        # Actual content (included by about.html)
└── posts/
    ├── list.html      # Blog list (full + HTMX)
    └── _list.html     # Actual content (included by list.html)
```
