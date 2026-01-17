@echo off
SETLOCAL

:: --- Nazwa venv ---
SET VENV_NAME=.venv_TOR_Textual

:: --- Sprawdzenie Pythona ---
python --version
IF ERRORLEVEL 1 (
    echo Python nie jest zainstalowany lub nie jest w PATH.
    pause
    EXIT /B 1
)

:: --- Tworzenie venv ---
IF NOT EXIST %VENV_NAME% (
    echo Tworzenie wirtualnego srodowiska %VENV_NAME%...
    python -m venv %VENV_NAME%
)

:: --- Aktywacja venv ---
call %VENV_NAME%\Scripts\activate.bat

:: --- Aktualizacja pip ---
python -m pip install --upgrade pip

:: --- Instalacja pakietow ---
IF EXIST requirements.txt (
    pip install -r requirements.txt --only-binary=:all:
) ELSE (
    echo Brak pliku requirements.txt!
)

:: --- Dezaktywacja venv ---
deactivate

echo.
echo Gotowe! Srodowisko %VENV_NAME% zostalo dezaktywowane.
pause
ENDLOCAL
