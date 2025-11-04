# Interactive PowerShell helper to set JAVA_HOME, SPARK_HOME and update User PATH
# You will be prompted for the actual paths. Run this as a normal user PowerShell (no admin required).

Write-Host "This script will set User-level environment variables (JAVA_HOME, SPARK_HOME, PYSPARK_PYTHON) and append bin paths to your User PATH." -ForegroundColor Cyan

$jdkPath = Read-Host "Enter your JDK installation folder (e.g. C:\\Program Files\\Java\\jdk-17.0.x)"
$sparkHome = Read-Host "Enter your Spark folder (e.g. C:\\spark\\spark-3.5.1-bin-hadoop3.3)"

if (-not (Test-Path $jdkPath)) {
    Write-Host "Warning: JDK path does not exist: $jdkPath" -ForegroundColor Yellow
}
if (-not (Test-Path $sparkHome)) {
    Write-Host "Warning: Spark path does not exist: $sparkHome" -ForegroundColor Yellow
}

[Environment]::SetEnvironmentVariable('JAVA_HOME', $jdkPath, 'User')
[Environment]::SetEnvironmentVariable('SPARK_HOME', $sparkHome, 'User')

# Append bin folders to the User PATH if not already present
$userPath = [Environment]::GetEnvironmentVariable('Path','User')
$javaBin = Join-Path $jdkPath 'bin'
$sparkBin = Join-Path $sparkHome 'bin'

if ($userPath -notlike "*${javaBin}*") {
    $userPath = "$userPath;$javaBin"
}
if ($userPath -notlike "*${sparkBin}*") {
    $userPath = "$userPath;$sparkBin"
}

[Environment]::SetEnvironmentVariable('Path', $userPath, 'User')

# Set PYSPARK_PYTHON to the current python executable
try {
    $pythonExe = (Get-Command python -ErrorAction Stop).Source
    [Environment]::SetEnvironmentVariable('PYSPARK_PYTHON', $pythonExe, 'User')
    Write-Host "Set PYSPARK_PYTHON to $pythonExe"
} catch {
    Write-Host "Could not find 'python' in PATH. Ensure Python is installed and in PATH before running PySpark." -ForegroundColor Yellow
}

Write-Host "Environment variables set at User scope. Please restart PowerShell / VS Code (or log out and log in) for changes to take effect." -ForegroundColor Green
