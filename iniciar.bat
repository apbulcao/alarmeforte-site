@echo off
echo Gerando site...
python build.py
echo.
echo Servidor local em http://localhost:8080
echo Pressione Ctrl+C para parar.
start http://localhost:8080
python -m http.server 8080
