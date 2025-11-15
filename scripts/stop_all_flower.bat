@echo off
REM Stop all Flower server and client processes

echo Stopping all Flower processes...

REM Kill Python processes running Flower server/client scripts
taskkill /F /FI "WINDOWTITLE eq Flower Server*" 2>nul
taskkill /F /FI "WINDOWTITLE eq Flower Client*" 2>nul

REM Kill processes using ports 8080-8084
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8080"') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8081"') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8082"') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8083"') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8084"') do taskkill /F /PID %%a 2>nul

timeout /t 2 /nobreak >nul

echo.
echo All Flower processes stopped.
echo.
pause

