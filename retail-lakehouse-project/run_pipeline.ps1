<#
.SYNOPSIS
    Run the complete Instacart Lakehouse ETL pipeline

.DESCRIPTION
    This script runs all three lakehouse layers in sequence:
    1. Bronze: Ingest CSV → Delta Lake
    2. Silver: Transform and enrich
    3. Gold: Create business metrics

.EXAMPLE
    .\run_pipeline.ps1
    Runs the complete pipeline

.EXAMPLE
    .\run_pipeline.ps1 -SkipBronze
    Skips bronze ingestion (data already loaded)
#>

param(
    [switch]$SkipBronze,
    [switch]$SkipSilver,
    [switch]$SkipGold
)

# Ensure script runs from its folder
Set-Location -Path $PSScriptRoot

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "INSTACART LAKEHOUSE ETL PIPELINE" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

# Check if venv exists
if (-not (Test-Path '.venv')) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: .\setup_venv.ps1" -ForegroundColor Yellow
    exit 1
}

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
. .venv\Scripts\Activate.ps1

# Check if raw data exists
if (-not (Test-Path 'data\raw\orders.csv')) {
    Write-Host "WARNING: Raw data files not found in data\raw\" -ForegroundColor Yellow
    Write-Host "Please download Instacart dataset and place CSV files in data\raw\" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne 'y') {
        exit 0
    }
}

# Track execution times
$startTime = Get-Date

# Step 1: Bronze Ingestion
if (-not $SkipBronze) {
    Write-Host ""
    Write-Host "[1/3] Running Bronze Layer Ingestion..." -ForegroundColor Green
    Write-Host "-" * 80
    $bronzeStart = Get-Date
    python scripts\01_bronze_ingestion.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Bronze ingestion failed!" -ForegroundColor Red
        exit 1
    }
    $bronzeTime = (Get-Date) - $bronzeStart
    Write-Host "✓ Bronze layer completed in $($bronzeTime.TotalSeconds.ToString('0.00'))s" -ForegroundColor Green
} else {
    Write-Host "[1/3] Skipping Bronze Layer (--SkipBronze)" -ForegroundColor Yellow
}

# Step 2: Silver Transformation
if (-not $SkipSilver) {
    Write-Host ""
    Write-Host "[2/3] Running Silver Layer Transformation..." -ForegroundColor Green
    Write-Host "-" * 80
    $silverStart = Get-Date
    python scripts\02_silver_transformation.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Silver transformation failed!" -ForegroundColor Red
        exit 1
    }
    $silverTime = (Get-Date) - $silverStart
    Write-Host "✓ Silver layer completed in $($silverTime.TotalSeconds.ToString('0.00'))s" -ForegroundColor Green
} else {
    Write-Host "[2/3] Skipping Silver Layer (--SkipSilver)" -ForegroundColor Yellow
}

# Step 3: Gold Aggregation
if (-not $SkipGold) {
    Write-Host ""
    Write-Host "[3/3] Running Gold Layer Aggregation..." -ForegroundColor Green
    Write-Host "-" * 80
    $goldStart = Get-Date
    python scripts\03_gold_aggregation.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Gold aggregation failed!" -ForegroundColor Red
        exit 1
    }
    $goldTime = (Get-Date) - $goldStart
    Write-Host "✓ Gold layer completed in $($goldTime.TotalSeconds.ToString('0.00'))s" -ForegroundColor Green
} else {
    Write-Host "[3/3] Skipping Gold Layer (--SkipGold)" -ForegroundColor Yellow
}

# Summary
$totalTime = (Get-Date) - $startTime
Write-Host ""
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "PIPELINE COMPLETED SUCCESSFULLY" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "Total execution time: $($totalTime.TotalMinutes.ToString('0.00')) minutes" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  - Explore data: jupyter notebook notebooks\instacart_analysis.ipynb" -ForegroundColor White
Write-Host "  - Check Gold metrics in: data\gold\" -ForegroundColor White
Write-Host ""
