# Contributing Guidelines

Thank you for your interest in contributing to the Inventory Management System! This document provides guidelines and instructions for contributing to this project.

## Development Process

1. **Branch Strategy**

   - `main`: Stable production code
   - `dev`: Development branch
   - `feature/*`: New features
   - `bugfix/*`: Bug fixes
   - `hotfix/*`: Urgent fixes for production

2. **Making Changes**

   ```bash
   # Create a new feature branch
   git checkout -b feature/your-feature-name

   # Make your changes
   git add .
   git commit -m "feat: your descriptive commit message"

   # Push your branch
   git push origin feature/your-feature-name
   ```

3. **Commit Message Format**

   - feat: New feature
   - fix: Bug fix
   - docs: Documentation changes
   - style: Code style changes (formatting, etc)
   - refactor: Code refactoring
   - test: Adding tests
   - chore: Maintenance tasks

4. **Pull Request Process**

   - Create PR against the `dev` branch
   - Provide clear description of changes
   - Reference any related issues
   - Ensure all tests pass
   - Request review from team members

5. **Code Review Guidelines**
   - Review for functionality
   - Check code style
   - Verify documentation
   - Test changes locally

## Setup Development Environment

1. **Fork and Clone**

   ```bash
   git clone https://github.com/zhengyang6751/inventory-management-system.git
   cd inventory-management-system
   ```

2. **Stay Updated**

   ```bash
   git remote add upstream https://github.com/zhengyang6751/inventory-management-system.git
   git fetch upstream
   git merge upstream/main
   ```

3. **Install Dependencies**
   Follow the setup instructions in README.md

## Testing

- Run backend tests: `cd backend && pytest`
- Run frontend tests: `cd frontend && npm test`

## Questions?

Feel free to open an issue or contact the maintainers if you have any questions.
