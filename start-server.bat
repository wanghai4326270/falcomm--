@echo off
chcp 65001 >nul
echo 正在启动本地服务器...
echo.
echo 服务器启动后，请在浏览器中访问：
echo http://localhost:8080
echo.
echo 按 Ctrl+C 停止服务器
echo.
cd /d %~dp0
python -m http.server 8080
pause

