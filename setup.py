"""
FieldTuner Setup Script
World-Class Battlefield 6 Configuration Tool
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="FieldTuner",
    version="1.0.0",
    author="Tom Stetson",
    author_email="tom@fieldtuner.com",
    description="World-Class Battlefield 6 Configuration Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/FieldTuner",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/FieldTuner/issues",
        "Source": "https://github.com/yourusername/FieldTuner",
        "Documentation": "https://github.com/yourusername/FieldTuner/wiki",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
    ],
    keywords="battlefield, gaming, configuration, settings, gui, pyqt6",
    python_requires=">=3.8",
    install_requires=[
        "PyQt6>=6.4.0",
        "pathlib2==2.3.7",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "pyinstaller>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "fieldtuner=src.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["assets/*.ico", "assets/*.png"],
    },
    zip_safe=False,
)
