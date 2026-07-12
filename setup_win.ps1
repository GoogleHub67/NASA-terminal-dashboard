Write-Host "Initializing NASA Terminal Dashboard Windows Deployment..." -ForegroundColor Cyan

# Verify Python installation
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python is not installed or not added to system PATH." -ForegroundColor Red
    Exit
}

Write-Host "Installing required package arrays from specifications..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "Environment installation complete. Launching terminal interface..." -ForegroundColor Green
    Start-Sleep -Seconds 2
    python nasa.py
} else {
    Write-Host "Deployment failed during dependency package installation." -ForegroundColor Red
}