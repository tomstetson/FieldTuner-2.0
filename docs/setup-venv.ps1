# FieldTuner 2.0 - Virtual Environment Setup Script
# Creates an isolated Python environment for this project

Write-Host "Setting up FieldTuner 2.0 development environment..." -ForegroundColor Cyan

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python not found. Please install Python 3.11 or later." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
python -m venv venv

if (Test-Path "venv") {
    Write-Host "✓ Virtual environment created successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

# Activate virtual environment and install requirements
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

Write-Host "`n✓ Setup complete!" -ForegroundColor Green
Write-Host "`nTo activate the virtual environment in the future, run:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "`nTo deactivate:" -ForegroundColor Cyan
Write-Host "  deactivate" -ForegroundColor White

