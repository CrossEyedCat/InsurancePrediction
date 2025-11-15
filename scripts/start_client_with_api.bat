@echo off
REM Start Flower client with HTTP API
REM Usage: start_client_with_api.bat <client_id> [http_port]

if "%1"=="" (
    echo Usage: %0 ^<client_id^> [http_port]
    echo Example: %0 1 8081
    exit /b 1
)

set CLIENT_ID=%1
set HTTP_PORT=%2
if "%HTTP_PORT%"=="" set HTTP_PORT=8081

cd /d "%~dp0\.."

set FLOWER_SERVER_URL=localhost:8080
set LOCAL_EPOCHS=5
set BATCH_SIZE=32
set LEARNING_RATE=0.001
set HTTP_PORT=%HTTP_PORT%

echo Starting Flower Client %CLIENT_ID% with HTTP API on port %HTTP_PORT%

python flower_client\client_with_api.py --client-id %CLIENT_ID% --server-address localhost:8080 --data-dir output --http-port %HTTP_PORT%

pause

