@echo off
REM Przejście do folderu z venv
cd /d "G:\RPG\The One Ring\Tool\The-One-Randomizer\.venv310\Scripts"

REM Aktywacja virtualenv
call activate.bat

REM Przejście do głównego folderu projektu
cd /d "G:\RPG\The One Ring\Tool\The-One-Randomizer"

REM Uruchomienie aplikacji
textual run --dev .\main_textual_app.py

pause
