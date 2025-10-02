@echo off
echo 🌌 NASA Exoplanet AI Platform - Local Development
echo ============================================================
echo.
echo 📋 Manual startup instructions:
echo.
echo 1. 啟動後端 (FastAPI):
echo    cd backend
echo    python ultra_simple_api.py
echo    或者: uvicorn ultra_simple_api:app --host 0.0.0.0 --port 8000 --reload
echo.
echo 2. 啟動前端 (React) - 新開一個終端:
echo    cd frontend  
echo    npm start
echo.
echo 3. 訪問應用:
echo    前端: http://localhost:3000
echo    後端API: http://localhost:8000
echo    後端文檔: http://localhost:8000/docs
echo.
echo ============================================================
echo 按任意鍵開始自動啟動...
pause

echo.
echo 🚀 Starting backend...
cd backend
start "Backend Server" cmd /k "python ultra_simple_api.py"

echo.
echo ⏳ Waiting for backend to start...
timeout /t 5 /nobreak

echo.
echo 🚀 Starting frontend...
cd ..\frontend
start "Frontend Server" cmd /k "npm start"

echo.
echo ✅ Both servers are starting!
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend: http://localhost:8000
echo.
echo Press any key to exit...
pause
