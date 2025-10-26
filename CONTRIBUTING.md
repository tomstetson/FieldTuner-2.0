# Contributing to FieldTuner

Thank you for your interest in contributing to FieldTuner! This document provides guidelines and information for contributors.

## 🚀 **Getting Started**

### **Prerequisites**
- Python 3.11 or higher
- PyQt6
- Git
- A code editor (VS Code, PyCharm, etc.)

### **Development Setup**

1. **Fork the repository**
   ```bash
   git fork https://github.com/sneakytom/FieldTuner.git
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/FieldTuner.git
   cd FieldTuner
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Run the application**
   ```bash
   python src/main_v2.py
   ```

## 🏗️ **Project Architecture**

### **Directory Structure**
```
FieldTuner/
├── src/
│   ├── core/           # Core business logic
│   ├── ui/             # User interface
│   ├── utils/          # Utility functions
│   └── main_v2.py      # Main entry point
├── tests/              # Test suite
├── docs/               # Documentation
└── assets/             # Static assets
```

### **Key Components**
- **Core**: Business logic and data management
- **UI**: User interface components and tabs
- **Utils**: Utility functions and helpers
- **Tests**: Comprehensive test suite

## 📝 **Development Guidelines**

### **Code Style**
- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Write clear, descriptive variable names
- Add docstrings to all functions and classes

### **Commit Messages**
Use clear, descriptive commit messages:
```
feat: add new preset system
fix: resolve profile detection issue
docs: update README with new features
```

### **Pull Request Process**

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, well-documented code
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   python -m pytest tests/
   python src/main_v2.py  # Manual testing
   ```

4. **Submit a pull request**
   - Provide a clear description of changes
   - Reference any related issues
   - Include screenshots for UI changes

## 🧪 **Testing**

### **Running Tests**
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_config_manager.py

# Run with coverage
python -m pytest --cov=src tests/
```

### **Writing Tests**
- Write tests for all new functionality
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies

### **Test Structure**
```python
def test_feature_name():
    """Test description."""
    # Arrange
    setup_test_data()
    
    # Act
    result = function_under_test()
    
    # Assert
    assert result == expected_value
```

## 🎨 **UI Development**

### **Adding New Tabs**
1. Create new tab file in `src/ui/tabs/`
2. Follow the existing tab structure
3. Add to `src/ui/tabs/__init__.py`
4. Register in main window

### **Component Guidelines**
- Use the existing component system
- Follow the design patterns
- Add proper error handling
- Include accessibility features

## 📚 **Documentation**

### **Code Documentation**
- Add docstrings to all public functions
- Include type hints
- Document complex algorithms
- Add inline comments for clarity

### **User Documentation**
- Update README.md for new features
- Add screenshots for UI changes
- Update installation instructions
- Document configuration options

## 🐛 **Bug Reports**

### **Before Reporting**
1. Check existing issues
2. Test with latest version
3. Gather relevant information

### **Bug Report Template**
```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: Windows 10/11
- Python Version: 3.11.x
- FieldTuner Version: 2.0.x

**Additional Context**
Any other relevant information
```

## 💡 **Feature Requests**

### **Before Requesting**
1. Check existing feature requests
2. Consider if it fits the project scope
3. Think about implementation complexity

### **Feature Request Template**
```markdown
**Feature Description**
Clear description of the requested feature

**Use Case**
Why would this feature be useful?

**Proposed Solution**
How could this feature be implemented?

**Alternatives**
Other ways to achieve the same goal

**Additional Context**
Any other relevant information
```

## 🔧 **Development Tools**

### **Recommended Tools**
- **IDE**: VS Code with Python extension
- **Version Control**: Git with GitHub Desktop
- **Testing**: pytest
- **Code Quality**: flake8, black
- **Documentation**: Sphinx

### **VS Code Extensions**
- Python
- PyQt6
- GitLens
- Python Docstring Generator
- autoDocstring

## 📋 **Code Review Process**

### **For Contributors**
- Respond to review feedback promptly
- Make requested changes
- Test changes thoroughly
- Update documentation

### **For Reviewers**
- Be constructive and helpful
- Focus on code quality and functionality
- Check for security issues
- Verify tests and documentation

## 🎯 **Contribution Areas**

### **High Priority**
- Bug fixes
- Performance improvements
- Documentation updates
- Test coverage improvements

### **Medium Priority**
- New features
- UI/UX improvements
- Code refactoring
- Plugin system development

### **Low Priority**
- Advanced features
- Experimental functionality
- Nice-to-have improvements

## 📞 **Getting Help**

### **Communication Channels**
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Requests**: Code contributions

### **Response Times**
- Bug reports: 1-3 days
- Feature requests: 1-2 weeks
- Pull requests: 3-7 days
- General questions: 1-5 days

## 📄 **License**

By contributing to FieldTuner, you agree that your contributions will be licensed under the MIT License.

## 🙏 **Recognition**

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation
- GitHub contributors page

Thank you for contributing to FieldTuner! Your efforts help make Battlefield 6 configuration easier for everyone.

---

**Made with ❤️ by the FieldTuner Community**