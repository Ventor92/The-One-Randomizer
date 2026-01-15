@echo off
REM Przejście do folderu z venv
cd /d ".venv_TOR_Textual\Scripts"

REM Aktywacja virtualenv
call activate.bat

REM Przejście do głównego folderu projektu
cd /d "..\..\textual_app"

REM Uruchomienie aplikacji
textual run --dev .\main_textual_app.py

pause
