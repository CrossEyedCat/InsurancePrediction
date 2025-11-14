@echo off
REM Start federated learning training - Updated version
REM Uses current Flower API (warnings are OK, code still works)

echo ========================================
echo Starting Federated Learning Training
echo ========================================
echo.
echo This will open 4 windows:
echo   1. Server (wait for it to start)
echo   2-4. Clients (will connect automatically)
echo.
pause

REM Set environment variables
set SERVER_ADDRESS=localhost
set SERVER_PORT=8080
set NUM_ROUNDS=5
set MIN_CLIENTS=3
set FRACTION_FIT=1.0
set FRACTION_EVALUATE=1.0
set MIN_AVAILABLE_CLIENTS=3
set LOCAL_EPOCHS=3
set BATCH_SIZE=32
set LEARNING_RATE=0.001

REM Start server in new window
echo Starting server...
start "Flower Server - Wait for 'gRPC server running'" cmd /k "cd /d %~dp0 && python flower_server\server.py"

REM Wait for server to start
echo Waiting 8 seconds for server to initialize...
timeout /t 8 /nobreak >nul

REM Start clients in separate windows
echo Starting clients...
start "Flower Client 1" cmd /k "cd /d %~dp0 && set FLOWER_SERVER_URL=localhost:8080 && set LOCAL_EPOCHS=3 && set BATCH_SIZE=32 && set LEARNING_RATE=0.001 && python flower_client\client.py --client-id 1 --server-address localhost:8080 --data-dir output"

timeout /t 2 /nobreak >nul

start "Flower Client 2" cmd /k "cd /d %~dp0 && set FLOWER_SERVER_URL=localhost:8080 && set LOCAL_EPOCHS=3 && set BATCH_SIZE=32 && set LEARNING_RATE=0.001 && python flower_client\client.py --client-id 2 --server-address localhost:8080 --data-dir output"

timeout /t 2 /nobreak >nul

start "Flower Client 3" cmd /k "cd /d %~dp0 && set FLOWER_SERVER_URL=localhost:8080 && set LOCAL_EPOCHS=3 && set BATCH_SIZE=32 && set LEARNING_RATE=0.001 && python flower_client\client.py --client-id 3 --server-address localhost:8080 --data-dir output"

echo.
echo ========================================
echo All windows opened!
echo ========================================
echo.
echo IMPORTANT:
echo 1. Check the SERVER window - it should show "gRPC server running"
echo 2. Check CLIENT windows - they should show "Loaded data successfully"
echo 3. Training will start automatically when all clients connect
echo 4. After training completes, check flower_server\models\ for saved models
echo.
echo The deprecation warnings are OK - the code still works!
echo.
echo Press any key to exit this window (training continues in other windows)...
pause >nul

