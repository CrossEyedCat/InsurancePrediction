@echo off
REM Start Flower server

cd /d "%~dp0\.."

set SERVER_ADDRESS=0.0.0.0
set SERVER_PORT=8080
set NUM_ROUNDS=10
set MIN_CLIENTS=3
set FRACTION_FIT=1.0
set FRACTION_EVALUATE=1.0
set LOCAL_EPOCHS=5
set BATCH_SIZE=32
set LEARNING_RATE=0.001

python flower_server\server.py

pause


