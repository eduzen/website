# My Django Blog: [eduzen.ar](http://eduzen.ar)

Welcome to my personal Django blog powered by htmx, a modern approach to full-stack development. This project is a blend of several technologies that aim to create a seamless blogging experience.

![Python application](https://github.com/eduzen/website/workflows/Python%20application/badge.svg)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

## Features

- **Django Backend**: The power of Django for the backend ensures stability and scalability.
- **htmx**: Integrating htmx for a seamless full-stack experience without writing JavaScript.
- **ChatGPT API**: Using the ChatGPT API for dynamic content creation and engagement.
- **GitHub Actions**: Continuous integration ensuring code quality and automatic deployments.
- **Dockerized**: The entire setup is containerized using Docker for consistent development and deployment.
- **Static Typing with Mypy**: Bringing the power of static typing to Python.
- **pip-tools**: Ensuring dependencies are managed in a reliable way.
- **Pre-commit**: Automated checks before commits to ensure code quality.

## Getting Started

### Prerequisites

Ensure you have Docker and Docker Compose installed on your system.

### Configuration

1. **Setup Environment Variables**:
   Copy the sample environment file and fill in your credentials:
   ```bash
   cp .env.sample .env

2. **Start the Application**:
  ```bash
  make start
  ```

3. **Database Migration**:
  ```bash
  make migrate
  ```

4. **View Logs**:
  ```bash
  make logs
  ```
