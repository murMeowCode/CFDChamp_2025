@echo off
chcp 65001 >nul

echo Starting microservices...

REM Запуск Auth Service
echo Starting Auth Service on port 8000...
cd auth_service\app
start "Auth Service" cmd /k "uvicorn main:app --port 8000"
cd ..\..

REM Запуск Profile Service  
echo Starting Profile Service on port 8001...
cd profile_service\app
start "Profile Service" cmd /k "uvicorn main:app --port 8001"
cd ..\..

REM Запуск Mailing Service
echo Starting Mailing Service on port 8002...
cd mailing_service\app
start "Mailing Service" cmd /k "uvicorn main:app --port 8002"
cd ..\..

echo All services started!
echo - Auth Service: http://127.0.0.1:8000
echo - Profile Service: http://127.0.0.1:8001
echo - Mailing Service: http://127.0.0.1:8002
echo.
echo Press any key to close this window...
pause >nul