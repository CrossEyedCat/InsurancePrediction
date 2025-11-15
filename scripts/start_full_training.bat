@echo off
REM Start full training with server, 3 clients, and monitoring
REM Opens each component in a separate window

echo ======================================================================
echo Starting Full Training with Monitoring
echo ======================================================================
echo.
echo This will start:
echo   - Flower server with monitoring (port 8080, HTTP API: 8082)
echo   - 3 Flower clients with monitoring (HTTP APIs: 8081, 8083, 8084)
echo   - Training for 5 rounds
echo.
echo Starting components...
echo.

REM Start server
echo Starting Flower Server...
start "Flower Server" cmd /k "cd /d %~dp0\.. && python flower_server\server_with_monitoring.py"

timeout /t 5 /nobreak >nul

REM Start clients
echo Starting Client 1...
start "Flower Client 1" cmd /k "cd /d %~dp0\.. && python flower_client\client_with_api.py --client-id 1 --server-address localhost:8080 --data-dir output --http-port 8081"

timeout /t 3 /nobreak >nul

echo Starting Client 2...
start "Flower Client 2" cmd /k "cd /d %~dp0\.. && python flower_client\client_with_api.py --client-id 2 --server-address localhost:8080 --data-dir output --http-port 8083"

timeout /t 3 /nobreak >nul

echo Starting Client 3...
start "Flower Client 3" cmd /k "cd /d %~dp0\.. && python flower_client\client_with_api.py --client-id 3 --server-address localhost:8080 --data-dir output --http-port 8084"

timeout /t 5 /nobreak >nul

echo.
echo ======================================================================
echo All components started!
echo ======================================================================
echo.
echo Monitoring endpoints:
echo   Server: http://localhost:8082/monitoring/status
echo   Client 1: http://localhost:8081/monitoring/status
echo   Client 2: http://localhost:8083/monitoring/status
echo   Client 3: http://localhost:8084/monitoring/status
echo.
echo To monitor training progress, run:
echo   python scripts\quick_monitoring_test.py
echo.
echo Or check monitoring in browser:
echo   Server: http://localhost:8082/monitoring/history
echo   Clients: http://localhost:8081/monitoring/history
echo.
pause

