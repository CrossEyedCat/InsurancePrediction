# PowerShell script to run federated learning
# Run this script to start training

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Federated Learning Training" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if data exists
if (-not (Test-Path "output\patients.csv")) {
    Write-Host "ERROR: Data directory 'output' not found!" -ForegroundColor Red
    exit 1
}

# Set environment variables
$env:SERVER_ADDRESS = "localhost"
$env:SERVER_PORT = "8080"
$env:NUM_ROUNDS = "5"
$env:MIN_CLIENTS = "3"
$env:FRACTION_FIT = "1.0"
$env:FRACTION_EVALUATE = "1.0"
$env:MIN_AVAILABLE_CLIENTS = "3"
$env:LOCAL_EPOCHS = "3"
$env:BATCH_SIZE = "32"
$env:LEARNING_RATE = "0.001"

# Start server in background
Write-Host "Starting server..." -ForegroundColor Yellow
$serverJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    python flower_server\server.py
}

Write-Host "Server started (Job ID: $($serverJob.Id))" -ForegroundColor Green
Write-Host "Waiting for server to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Start clients
Write-Host "`nStarting clients..." -ForegroundColor Yellow
$clientJobs = @()

for ($i = 1; $i -le 3; $i++) {
    Write-Host "  Starting client $i..." -ForegroundColor Yellow
    $clientJob = Start-Job -ScriptBlock {
        param($clientId, $pwd)
        Set-Location $pwd
        $env:FLOWER_SERVER_URL = "localhost:8080"
        python flower_client\client.py --client-id $clientId --server-address localhost:8080 --data-dir output
    } -ArgumentList $i, $PWD
    
    $clientJobs += $clientJob
    Write-Host "  Client $i started (Job ID: $($clientJob.Id))" -ForegroundColor Green
    Start-Sleep -Seconds 2
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "All processes started!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Server Job ID: $($serverJob.Id)" -ForegroundColor Green
for ($i = 0; $i -lt $clientJobs.Count; $i++) {
    Write-Host "Client $($i+1) Job ID: $($clientJobs[$i].Id)" -ForegroundColor Green
}
Write-Host "`nTraining in progress..." -ForegroundColor Yellow
Write-Host "Monitor progress with: Get-Job | Receive-Job" -ForegroundColor Cyan
Write-Host ""

# Wait for server to complete
Write-Host "Waiting for training to complete..." -ForegroundColor Yellow
Wait-Job $serverJob | Out-Null

Write-Host "`nServer completed!" -ForegroundColor Green

# Wait a bit for clients
Start-Sleep -Seconds 3

# Stop clients
Write-Host "Stopping clients..." -ForegroundColor Yellow
$clientJobs | Stop-Job
$clientJobs | Remove-Job

# Check for models
Write-Host "`nChecking for models..." -ForegroundColor Yellow
if (Test-Path "flower_server\models\*.pt") {
    Write-Host "`nModels created:" -ForegroundColor Green
    Get-ChildItem flower_server\models\*.pt | ForEach-Object {
        $sizeMB = [math]::Round($_.Length / 1MB, 2)
        Write-Host "  - $($_.Name) ($sizeMB MB)" -ForegroundColor Green
    }
} else {
    Write-Host "No models found. Check logs for errors." -ForegroundColor Red
    Write-Host "`nServer output:" -ForegroundColor Yellow
    Receive-Job $serverJob
}

Remove-Job $serverJob

Write-Host "`nDone!" -ForegroundColor Cyan

