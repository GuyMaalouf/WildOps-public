# Contributing to WildOps

First off, thank you for considering contributing to WildOps! It's people like you that make WildOps such a great tool for wildlife conservation.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Pledge

We are committed to making participation in this project a harassment-free experience for everyone, regardless of level of experience, gender, gender identity and expression, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, religion, or nationality.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as much detail as possible.
* **Provide specific examples to demonstrate the steps**.
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**
* **Include screenshots and animated GIFs** if possible.
* **Include your environment details**: OS, Python version, Django version, browser, etc.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title** for the issue to identify the suggestion.
* **Provide a step-by-step description of the suggested enhancement** in as much detail as possible.
* **Provide specific examples to demonstrate the steps** or provide mockups.
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
* **Explain why this enhancement would be useful** to most WildOps users.

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Follow the Python and Django style guides
* Include thoughtful commit messages
* Include appropriate test coverage
* Update documentation as needed
* End all files with a newline

## Development Process

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/wildops_public.git
   cd wildops_public
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Run migrations**:
   ```bash
   cd WildOpsProject
   python manage.py migrate
   python manage.py create_groups
   ```

7. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

### Creating a Branch

Create a branch for your work:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Branch naming conventions:
* `feature/` - for new features
* `fix/` - for bug fixes
* `docs/` - for documentation changes
* `refactor/` - for code refactoring
* `test/` - for adding tests

### Making Changes

1. **Write clean, readable code** following PEP 8 guidelines
2. **Add comments** where necessary to explain complex logic
3. **Write or update tests** for your changes
4. **Update documentation** if you're changing functionality
5. **Keep commits atomic** - one logical change per commit

### Code Style Guidelines

#### Python/Django

* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Use 4 spaces for indentation (not tabs)
* Maximum line length: 100 characters
* Use descriptive variable names
* Add docstrings to functions and classes
* Follow Django best practices and conventions

Example:
```python
def calculate_operation_area(latitude, longitude, radius):
    """
    Calculate the area covered by a drone operation.
    
    Args:
        latitude (float): Center point latitude
        longitude (float): Center point longitude
        radius (float): Operation radius in meters
        
    Returns:
        float: Area in square meters
    """
    # Implementation here
    pass
```

#### JavaScript

* Use ES6+ features where appropriate
* Use 2 spaces for indentation
* Use meaningful variable names
* Add comments for complex logic

#### HTML/CSS

* Use semantic HTML5 elements
* Keep CSS organized and commented
* Follow BEM naming convention when possible
* Ensure responsive design

### Testing

* Write tests for new features
* Ensure all tests pass before submitting PR
* Run tests with:
  ```bash
  python manage.py test
  ```

### Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

Examples:
```
Add weather threshold validation

- Implement min/max value checks
- Add user feedback for invalid inputs
- Update tests

Fixes #123
```

### Submitting Changes

1. **Push your changes** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a Pull Request** from your fork to the main repository

3. **Fill out the PR template** completely

4. **Wait for review** - maintainers will review your PR and may request changes

5. **Make requested changes** if any, and push them to your branch

6. **Once approved**, your PR will be merged!

## Project Structure

Understanding the project structure will help you contribute effectively:

```
WildOpsProject/
├── accounts/              # User authentication and management
│   ├── models.py         # User models
│   ├── views.py          # Authentication views
│   └── forms.py          # Login/registration forms
├── MapApp/               # Operation mapping functionality
│   ├── models.py         # Operation models
│   ├── views.py          # Map and operation views
│   └── forms.py          # Operation forms
├── WildProcedures/       # Checklist generation
│   ├── models.py         # Procedure models
│   ├── views.py          # Checklist views
│   ├── checklist_generator.py  # PDF generation
│   └── data/json/        # Procedure data files
├── weather_check/        # Weather monitoring
│   ├── models.py         # Weather models
│   ├── views.py          # Weather views
│   └── data/json/        # Weather threshold config
└── shared/               # Shared utilities
    └── constants.py      # Shared constants
```

## Areas We Need Help With

* **Testing**: More comprehensive test coverage
* **Documentation**: Improving documentation and adding examples
* **Internationalization**: Translating the interface to other languages
* **Mobile Support**: Improving mobile responsiveness
* **Performance**: Optimizing database queries and page load times
* **Accessibility**: Improving WCAG compliance
* **UI/UX**: Enhancing user interface and experience
* **Integration**: Adding support for more UAS platforms and APIs

## Feature Requests and Roadmap

Check our [roadmap](README.md#roadmap) to see what we're planning. Feel free to suggest new features through GitHub Issues!

## Questions?

Don't hesitate to ask questions! You can:
* Open an issue with your question
* Start a discussion in GitHub Discussions
* Contact the maintainers

## Recognition

Contributors will be recognized in our README and release notes. We appreciate every contribution, no matter how small!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to WildOps! Your efforts help improve wildlife conservation technology. 🦁🚁
