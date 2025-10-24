# Contributing to FieldTuner

Thank you for your interest in contributing to FieldTuner! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- Git
- A GitHub account

### Development Setup
1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/FieldTuner.git
   cd FieldTuner
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```
4. Run the application:
   ```bash
   python src/main.py
   ```

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Write clear, descriptive variable and function names
- Add docstrings to all functions and classes

### Commit Messages
Use clear, descriptive commit messages:
- `feat: add new feature`
- `fix: resolve bug`
- `docs: update documentation`
- `style: code formatting`
- `refactor: code restructuring`
- `test: add or update tests`

### Pull Request Process
1. Create a feature branch from `main`
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Update documentation if needed
6. Submit a pull request

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_config_manager.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Writing Tests
- Write tests for all new functionality
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies

## 🎨 UI/UX Guidelines

### Design Principles
- Follow WeMod-inspired design patterns
- Maintain consistency with existing UI
- Ensure accessibility
- Test on different screen sizes

### UI Components
- Use consistent styling
- Follow the established color scheme
- Maintain proper spacing and alignment
- Ensure responsive design

## 🐛 Bug Reports

When reporting bugs, please include:
- Operating system and version
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Log files from the Debug tab

## ✨ Feature Requests

When requesting features:
- Describe the use case
- Explain the expected behavior
- Consider the impact on existing functionality
- Provide mockups or examples if possible

## 📚 Documentation

### Code Documentation
- Add docstrings to all functions and classes
- Include type hints
- Document complex algorithms
- Update README for new features

### User Documentation
- Update user guides for new features
- Add screenshots for UI changes
- Update installation instructions
- Maintain changelog

## 🔧 Build and Release

### Building Executable
```bash
# Build portable executable
python build.py

# The executable will be created in dist/FieldTuner.exe
```

### Release Process
1. Update version numbers in `pyproject.toml`
2. Update changelog
3. Create release tag: `git tag -a v1.x.x -m "Release v1.x.x"`
4. Build and test executable
5. Create GitHub release

## 📋 Code Review Process

### For Contributors
- Ensure your code follows the style guidelines
- Add appropriate tests
- Update documentation
- Respond to review feedback

### For Reviewers
- Check code quality and style
- Verify tests are adequate
- Ensure documentation is updated
- Test the changes locally

## 🤝 Community Guidelines

### Be Respectful
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Focus on what's best for the community
- Show empathy towards other community members

### Be Constructive
- Provide helpful feedback
- Suggest improvements
- Share knowledge and experience
- Help others learn and grow

## 📞 Getting Help

- GitHub Issues for bug reports and feature requests
- GitHub Discussions for questions and general discussion
- Pull requests for code contributions

## 📄 License

By contributing to FieldTuner, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to FieldTuner! 🎮