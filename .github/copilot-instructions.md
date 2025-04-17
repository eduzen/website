You are an expert in Python, Django, and scalable web application development.

# Dependencies:

- uv
- Python 3.13
- Django 5.2
- HTMX
- Tailwind CSS
- Alpine.js
- PostgreSQL
- Redis

## Style Guide

Follow PEP 8 style guidelines. Include type hints (python > 3.13) for function parameters and return types. Write docstrings for all public modules, classes, functions, and methods.

## Key Principles

- Write clean, maintainable, and efficient code.
- Follow the DRY (Don't Repeat Yourself) principle to avoid code duplication.
- Use Django's built-in features and tools wherever possible to leverage its full capabilities.
- Use descriptive variable and function names; adhere to naming conventions (e.g., lowercase with underscores for functions and variables).
- Structure your project in a modular way using Django apps to promote reusability and separation of concerns.
- Leverage Django’s ORM for database interactions; avoid raw SQL queries unless necessary for performance.
- Use Django’s built-in user model and authentication framework for user management.
- Use middleware judiciously to handle cross-cutting concerns like authentication, logging, and caching.

## Error Handling and Validation

- Implement error handling at the view level and use Django's built-in error handling mechanisms.
- Use Django's validation framework to validate form and model data.
- Prefer try-except blocks for handling exceptions in business logic and views.
- Customize error pages (e.g., 404, 500) to improve user experience and provide helpful information.
- Use Django signals to decouple error handling and logging from core business logic.

## Django-Specific Guidelines

- Use Django templates for rendering HTML and DRF serializers for JSON responses.
- Keep business logic in models and forms; keep views light and focused on request handling.
- Use Django's URL dispatcher (urls.py) to define clear and RESTful URL patterns.
- Apply Django's security best practices (e.g., CSRF protection, SQL injection protection, XSS prevention).
- Use Django’s built-in tools for testing (unittest and pytest-django) to ensure code quality and reliability.
- Leverage Django’s caching framework to optimize performance for frequently accessed data.
- Use Django’s middleware for common tasks such as authentication, logging, and security.

## Performance Optimization

- Optimize query performance using Django ORM's select_related and prefetch_related for related object fetching.
- Use Django’s cache framework with backend support (e.g., Redis or Memcached) to reduce database load.
- Implement database indexing and query optimization techniques for better performance.
- Use asynchronous views and background tasks (via Celery) for I/O-bound or long-running operations.
- Optimize static file handling with Django’s static file management system (e.g., WhiteNoise or CDN integration).

## Key Conventions

1. Follow Django's "Convention Over Configuration" principle for reducing boilerplate code.
2. Prioritize security and performance optimization in every stage of development.
3. Maintain a clear and logical project structure to enhance readability and maintainability.

Refer to Django documentation for best practices in views, models, forms, and security considerations.
