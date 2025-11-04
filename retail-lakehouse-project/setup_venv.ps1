<#
Interactive helper to create a virtual environment, install requirements, and register an ipykernel.
Run this from inside the `retail-lakehouse-project` folder.
Usage: Open PowerShell, cd into retail-lakehouse-project, then run:
    .\setup_venv.ps1

This script will:
- create a .venv virtual environment (if missing)
- activate it for the current session
- upgrade pip and install packages from requirements.txt
- register the venv as a Jupyter kernel named 'retail-lakehouse-project'
#>

# Ensure script runs from its folder
Set-Location -Path $PSScriptRoot

if (-not (Test-Path '.venv')) {
    Write-Host "Creating virtual environment .venv..." -ForegroundColor Cyan
    python -m venv .venv
} else {
    Write-Host ".venv already exists." -ForegroundColor Yellow
}

Write-Host "Activating virtual environment..." -ForegroundColor Cyan
. .venv\Scripts\Activate.ps1

Write-Host "Upgrading pip and installing requirements..." -ForegroundColor Cyan
python -m pip install --upgrade pip
if (Test-Path 'requirements.txt') {
    pip install -r requirements.txt
} else {
    Write-Host "requirements.txt not found in the folder." -ForegroundColor Red
}

Write-Host "Registering ipykernel (for Jupyter)..." -ForegroundColor Cyan
python -m ipykernel install --user --name retail-lakehouse-project --display-name "Retail Lakehouse (.venv)"

Write-Host 'Done. Activate the venv in a new PowerShell with: . .venv\Scripts\Activate.ps1' -ForegroundColor Green
