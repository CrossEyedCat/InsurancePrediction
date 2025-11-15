@echo off
REM Start Flower server and client with monitoring
REM This script starts them in separate windows

echo Starting Flower Server with Monitoring...
start "Flower Server" cmd /k "cd /d %~dp0\.. && python flower_server\server_with_monitoring.py"

timeout /t 3 /nobreak >nul

echo Starting Flower Client 1 with Monitoring...
start "Flower Client 1" cmd /k "cd /d %~dp0\.. && python flower_client\client_with_api.py --client-id 1 --server-address localhost:8080 --data-dir output --http-port 8081"

timeout /t 5 /nobreak >nul

echo.
echo Server and client started in separate windows.
echo.
echo Monitoring endpoints:
echo   Server: http://localhost:8082/monitoring/status
echo   Client: http://localhost:8081/monitoring/status
echo.
echo To test monitoring, run:
echo   python scripts\quick_monitoring_test.py
echo.
pause

