# Contributing to StudySync

Thank you for your interest in contributing to StudySync! This document provides guidelines and instructions for contributing to the project.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A code editor (VS Code recommended)
- Basic knowledge of Python and web development

### Development Setup

1. **Fork the repository**

   ```bash
   # Fork the repo on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/gwc-studyplanner-.git
   cd gwc-studyplanner-
   ```

2. **Set up virtual environment**

   ```bash
   python -m venv studysync-env

   # On Windows:
   studysync-env\Scripts\activate
   # On macOS/Linux:
   source studysync-env/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # When available
   ```

4. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run tests**
   ```bash
   pytest
   ```

## 🏗️ Project Structure

```
StudySync/
├── src/
│   ├── core/           # Core business logic
│   ├── api/            # REST API endpoints
│   ├── ui/             # User interfaces (CLI, web)
│   └── utils/          # Utility functions
├── tests/              # Test files
├── docs/               # Documentation
├── main.py             # Application entry point
└── requirements.txt    # Python dependencies
```

## 🔄 Development Workflow

### Branching Strategy

- `main` - Production-ready code
- `develop` - Development branch for integration
- `feature/feature-name` - Feature development
- `fix/bug-description` - Bug fixes
- `docs/documentation-update` - Documentation updates

### Making Changes

1. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**

   - Write clean, readable code
   - Follow Python PEP 8 style guidelines
   - Add docstrings to functions and classes
   - Write tests for new functionality

3. **Test your changes**

   ```bash
   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=src

   # Test specific functionality
   python main.py --help
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add session reminder functionality"
   ```

### Commit Message Guidelines

Use conventional commit messages:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:

- `feat: add email notification support`
- `fix: resolve session scheduling conflict`
- `docs: update API documentation`
- `test: add unit tests for storage module`

## 🧪 Testing Guidelines

### Writing Tests

- Place test files in the `tests/` directory
- Name test files as `test_module_name.py`
- Use descriptive test function names
- Include both positive and negative test cases
- Mock external dependencies

### Test Categories

1. **Unit Tests** - Test individual functions/methods
2. **Integration Tests** - Test component interactions
3. **API Tests** - Test REST API endpoints
4. **CLI Tests** - Test command-line interface

### Example Test

```python
def test_create_study_group():
    """Test creating a new study group"""
    storage = Storage("sqlite:///:memory:")

    group_data = {
        'name': 'Test Group',
        'description': 'Test description',
        'max_members': 10
    }

    group_id = storage.create_group(group_data)
    assert group_id is not None

    retrieved = storage.get_group_by_id(group_id)
    assert retrieved['name'] == group_data['name']
```

## 📝 Code Style Guidelines

### Python Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Maximum line length: 88 characters (Black formatter)
- Use meaningful variable and function names

### Docstring Format

```python
def schedule_session(group_id: str, topic: str, start_time: datetime) -> str:
    """
    Schedule a new study session for a group.

    Args:
        group_id: The ID of the study group
        topic: The session topic/subject
        start_time: When the session should start

    Returns:
        str: The generated session ID

    Raises:
        ValueError: If the start time is in the past
        NotFoundError: If the group doesn't exist
    """
```

## 🌟 Types of Contributions

### 🐛 Bug Reports

When reporting bugs, please include:

- Clear description of the issue
- Steps to reproduce the problem
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Error messages or logs

### 💡 Feature Requests

For feature requests, please provide:

- Clear description of the feature
- Use case and motivation
- Proposed implementation approach
- Any related issues or discussions

### 📖 Documentation

Documentation improvements are always welcome:

- Fix typos and grammatical errors
- Add code examples
- Improve API documentation
- Add tutorials or guides
- Translate documentation

### 🔧 Code Contributions

Areas where contributions are especially welcome:

1. **Core Features**

   - Session management improvements
   - Notification system enhancements
   - Analytics and reporting

2. **Integrations**

   - Calendar integrations (Google, Outlook)
   - Chat platforms (Slack, Discord, Teams)
   - Learning management systems

3. **User Interface**

   - Web dashboard
   - Mobile app
   - CLI improvements

4. **Performance & Reliability**
   - Database optimization
   - Error handling
   - Logging improvements

## 🔍 Review Process

### Pull Request Guidelines

1. **Before submitting:**

   - Ensure all tests pass
   - Update documentation if needed
   - Check code style with linting tools
   - Rebase on latest main branch

2. **Pull request description:**

   - Clear title and description
   - Link related issues
   - List changes made
   - Include screenshots for UI changes

3. **Review process:**
   - At least one code review required
   - All CI checks must pass
   - Documentation must be updated
   - Breaking changes need special approval

### Code Review Checklist

**For reviewers:**

- [ ] Code follows project conventions
- [ ] Tests are comprehensive and pass
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed
- [ ] Backward compatibility maintained

## 🏷️ Issue Labels

We use labels to categorize issues:

- `bug` - Something isn't working
- `enhancement` - New feature or improvement
- `documentation` - Documentation needs
- `good first issue` - Good for newcomers
- `help wanted` - Community help needed
- `priority: high/medium/low` - Issue priority
- `status: in-progress` - Being worked on
- `type: question` - Questions about usage

## 🎯 Good First Issues

New contributors should look for issues labeled:

- `good first issue` - Beginner-friendly
- `documentation` - Documentation improvements
- `help wanted` - Community assistance needed

## 💬 Communication

### Getting Help

- **GitHub Issues** - Bug reports and feature requests
- **Discord** - Real-time discussion and questions
- **Email** - Security issues and private matters

### Code of Conduct

Please note that this project follows a Code of Conduct. Be respectful and inclusive in all interactions.

## 🏆 Recognition

Contributors will be recognized in:

- README.md contributors section
- CHANGELOG.md for significant contributions
- Annual contributor appreciation posts

Thank you for contributing to StudySync! 🎓📚
