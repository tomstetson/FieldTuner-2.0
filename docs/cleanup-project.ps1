# FieldTuner 2.0 Project Cleanup Script
# Moves development documentation files to appropriate locations

Write-Host "Cleaning up FieldTuner 2.0 project..." -ForegroundColor Cyan

# List of files to move
$filesToMove = @(
    "ARCHITECTURE_REVIEW_V2.md",
    "BF6_FEATURES_SUMMARY.md",
    "FEATURE_COMPARISON_V1_VS_V2.md",
    "PROJECT_CLEANUP_SUMMARY.md",
    "V2_FEATURE_RESTORATION_SUMMARY.md",
    "VALIDATION_V2_VS_V1.md",
    "CLEANUP_SUMMARY.md"
)

# Destination directory
$destination = "docs\development-notes"

# Ensure destination exists
if (-not (Test-Path $destination)) {
    New-Item -ItemType Directory -Path $destination -Force | Out-Null
}

# Move files
foreach ($file in $filesToMove) {
    if (Test-Path $file) {
        Write-Host "Moving $file..." -ForegroundColor Yellow
        Move-Item -Path $file -Destination $destination -Force
        Write-Host "  ✓ Moved successfully" -ForegroundColor Green
    } else {
        Write-Host "  ⊗ $file not found" -ForegroundColor DarkGray
    }
}

Write-Host "`nCleanup complete!" -ForegroundColor Green

