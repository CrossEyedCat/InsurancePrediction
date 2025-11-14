@echo off
REM Start Flower client
REM Usage: start_client.bat <client_id>

if "%1"=="" (
    echo Usage: %0 ^<client_id^>
    echo Example: %0 1
    exit /b 1
)

set CLIENT_ID=%1

cd /d "%~dp0\.."

set FLOWER_SERVER_URL=localhost:8080
set LOCAL_EPOCHS=5
set BATCH_SIZE=32
set LEARNING_RATE=0.001

python flower_client\client.py --client-id %CLIENT_ID% --server-address localhost:8080 --data-dir output

pause


