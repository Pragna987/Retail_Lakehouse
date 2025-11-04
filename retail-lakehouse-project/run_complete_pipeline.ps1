# Run Complete Lakehouse Pipeline
# Executes all stages of the data lakehouse implementation

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  DATA LAKEHOUSE PIPELINE - Complete Execution" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Virtual environment not detected" -ForegroundColor Yellow
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    
    if (Test-Path ".\.venv\Scripts\Activate.ps1") {
        & ".\.venv\Scripts\Activate.ps1"
        Write-Host "✓ Virtual environment activated`n" -ForegroundColor Green
    } else {
        Write-Host "❌ Virtual environment not found. Please run setup_venv.ps1 first" -ForegroundColor Red
        exit 1
    }
}

# Run the master Python script
Write-Host "Starting pipeline execution...`n" -ForegroundColor Green

python run_all.py

# Check exit code
if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Pipeline completed successfully!" -ForegroundColor Green
} else {
    Write-Host "`n❌ Pipeline failed with exit code: $LASTEXITCODE" -ForegroundColor Red
}

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
