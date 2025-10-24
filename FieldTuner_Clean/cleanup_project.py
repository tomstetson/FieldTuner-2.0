#!/usr/bin/env python3
"""
FieldTuner Project Cleanup Script
Organizes the project structure and prepares for GitHub
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def cleanup_project():
    """Clean up the project structure for GitHub."""
    print("FieldTuner Project Cleanup")
    print("=" * 30)
    
    # Create necessary directories
    directories = [
        "assets",
        "assets/screenshots", 
        "docs",
        "tests",
        "tests/fixtures",
        ".github/workflows",
        ".github/ISSUE_TEMPLATE",
        ".github/PULL_REQUEST_TEMPLATE"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   Created directory: {directory}")
    
    # Clean up build artifacts
    cleanup_directories = ["build", "dist", "__pycache__", "temp"]
    for directory in cleanup_directories:
        if Path(directory).exists():
            try:
                shutil.rmtree(directory)
                print(f"   Cleaned directory: {directory}")
            except PermissionError:
                print(f"   Warning: Could not clean {directory} (permission denied)")
    
    # Create placeholder files
    placeholder_files = {
        "assets/icon.ico": "# Placeholder for application icon",
        "assets/logo.png": "# Placeholder for logo image",
        "assets/screenshots/README.md": "# Screenshots for documentation",
        "tests/fixtures/README.md": "# Test fixtures and sample data",
        ".github/ISSUE_TEMPLATE/bug_report.md": "# Bug report template",
        ".github/ISSUE_TEMPLATE/feature_request.md": "# Feature request template",
        ".github/PULL_REQUEST_TEMPLATE/pull_request_template.md": "# Pull request template"
    }
    
    for file_path, content in placeholder_files.items():
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"   Created placeholder: {file_path}")
    
    # Create GitHub issue templates
    create_issue_templates()
    
    # Create GitHub PR template
    create_pr_template()
    
    # Create GitHub workflows
    create_github_workflows()
    
    # Create documentation files
    create_documentation()
    
    print("\nProject cleanup completed!")
    print("Ready for GitHub submission!")
    
    return True

def create_issue_templates():
    """Create GitHub issue templates."""
    
    # Bug report template
    bug_template = """---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**System Information**
- OS: [e.g. Windows 10, Windows 11]
- FieldTuner Version: [e.g. 1.0.0]
- Battlefield 6 Version: [e.g. Latest]
- Python Version: [e.g. 3.11] (if running from source)

**Additional context**
Add any other context about the problem here.
"""
    
    with open(".github/ISSUE_TEMPLATE/bug_report.md", "w", encoding="utf-8") as f:
        f.write(bug_template)
    
    # Feature request template
    feature_template = """---
name: Feature request
about: Suggest an idea for this project
title: ''
labels: enhancement
assignees: ''

---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
"""
    
    with open(".github/ISSUE_TEMPLATE/feature_request.md", "w", encoding="utf-8") as f:
        f.write(feature_template)

def create_pr_template():
    """Create GitHub pull request template."""
    
    pr_template = """## Description
Brief description of the changes in this PR.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Testing
- [ ] I have tested these changes locally
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## Screenshots (if applicable)
Add screenshots to help explain your changes.

## Additional Notes
Any additional information that reviewers should know.
"""
    
    with open(".github/PULL_REQUEST_TEMPLATE/pull_request_template.md", "w", encoding="utf-8") as f:
        f.write(pr_template)

def create_github_workflows():
    """Create GitHub workflow files."""
    
    # Build workflow
    build_workflow = """name: Build and Test

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/ -v
    
    - name: Build executable
      run: |
        python build_simple.py
    
    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: FieldTuner-Portable
        path: releases/
"""
    
    with open(".github/workflows/build.yml", "w", encoding="utf-8") as f:
        f.write(build_workflow)
    
    # Release workflow
    release_workflow = """name: Create Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Build executable
      run: |
        python build_simple.py
    
    - name: Create release package
      run: |
        python create_release.py
    
    - name: Create Release
      uses: softprops/action-gh-release@v1
      with:
        files: releases/*.zip
        generate_release_notes: true
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
"""
    
    with open(".github/workflows/release.yml", "w", encoding="utf-8") as f:
        f.write(release_workflow)

def create_documentation():
    """Create additional documentation files."""
    
    # User guide
    user_guide = """# FieldTuner User Guide

## Getting Started

### First Launch
1. Run FieldTuner as administrator
2. The application will automatically detect your Battlefield 6 config
3. A backup will be created automatically
4. You can start configuring your settings

### Quick Settings
- Choose from 5 optimized presets
- Apply settings with one click
- Fine-tune individual settings as needed

### Advanced Settings
- Access technical settings with user-friendly descriptions
- Modify specific configuration values
- Save custom presets

### Backup Management
- View all available backups
- Restore from any backup
- Create new backups with custom names
- Delete old backups

## Troubleshooting

### Common Issues
- Config file not found
- Permission denied errors
- Settings not applying

### Debug Mode
- Use the Debug tab for real-time logs
- Check error messages and warnings
- Export logs for support

## Tips and Tricks
- Always backup before making changes
- Test settings in a safe environment
- Keep multiple backup versions
- Use presets as starting points
"""
    
    with open("docs/user-guide.md", "w", encoding="utf-8") as f:
        f.write(user_guide)
    
    # API reference
    api_reference = """# FieldTuner API Reference

## ConfigManager

### Methods
- `detect_config()`: Detect Battlefield 6 config file
- `load_config()`: Load configuration from file
- `save_config()`: Save configuration to file
- `create_backup(name)`: Create a backup with optional name
- `restore_backup(path)`: Restore from backup file
- `list_backups()`: List all available backups

### Properties
- `config_path`: Path to the config file
- `settings`: Dictionary of current settings
- `BACKUP_DIR`: Path to backup directory

## UI Components

### MainWindow
- Main application window
- Tab management
- Event handling

### QuickSettingsTab
- Preset management
- Quick configuration
- Toggle switches

### GraphicsTab
- Graphics settings
- Resolution management
- Quality settings

### BackupTab
- Backup creation
- Backup restoration
- Backup management

## Events and Signals
- `settings_changed`: Emitted when settings are modified
- `backup_created`: Emitted when backup is created
- `config_loaded`: Emitted when config is loaded
"""
    
    with open("docs/api-reference.md", "w", encoding="utf-8") as f:
        f.write(api_reference)

if __name__ == "__main__":
    cleanup_project()
