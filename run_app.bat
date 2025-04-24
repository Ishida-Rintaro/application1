@echo off
REM Pythonのパスを指定
set PYTHON_PATH=C:\Users\irin_\AppData\Local\Programs\Python\Python312\python.exe

REM プロジェクトのパスを指定
set APP_PATH=c:\Users\irin_\OneDrive\ドキュメント\デスクトップ\application1

REM WaitressでFlaskアプリを起動
cd %APP_PATH%
%PYTHON_PATH% -m waitress --host=0.0.0.0 --port=5000 python_stocks:app
pause