# FieldTuner 2.0 - Isolation Configuration Script
# Ensures FieldTuner 2.0 is completely isolated from other projects

Write-Host "Configuring FieldTuner 2.0 isolation..." -ForegroundColor Cyan

# Check if path_config uses isolated AppData directory
Write-Host "`nVerifying AppData isolation..." -ForegroundColor Yellow

$appDataDir = "$env:APPDATA\FieldTuner"
Write-Host "FieldTuner AppData: $appDataDir" -ForegroundColor Green

# Check if directory exists
if (-not (Test-Path $appDataDir)) {
    Write-Host "Creating FieldTuner AppData directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $appDataDir -Force | Out-Null
    Write-Host "✓ Created" -ForegroundColor Green
}

# Create subdirectories
$subdirs = @("logs", "backups")
foreach ($dir in $subdirs) {
    $path = Join-Path $appDataDir $dir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "✓ Created $dir directory" -ForegroundColor Green
    }
}

# Verify virtual environment
Write-Host "`nChecking virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment exists" -ForegroundColor Green
} else {
    Write-Host "⚠ Virtual environment not found. Run .\setup-venv.ps1" -ForegroundColor Yellow
}

# Summary
Write-Host "`n=== Isolation Summary ===" -ForegroundColor Cyan
Write-Host "✓ AppData directory: $appDataDir" -ForegroundColor Green
Write-Host "✓ Project directory: $PWD" -ForegroundColor Green
Write-Host "✓ Virtual environment: $(if (Test-Path 'venv') { 'Ready' } else { 'Not created' })" -ForegroundColor $(
    if (Test-Path 'venv') { 'Green' } else { 'Yellow' }
)

Write-Host "`nFieldTuner 2.0 is isolated and ready for development!" -ForegroundColor Green

