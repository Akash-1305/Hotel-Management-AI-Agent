@echo off
echo ========================================
echo Hotel Management System Setup (Windows)
echo ========================================

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH. Please install Python and try again.
    exit /b 1
)

:: Create virtual environment
echo.
echo Setting up virtual environment...
python -m venv venv

:: Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies
echo.
echo Installing dependencies...
pip install langchain langgraph langchain-openai python-dotenv

:: Install required API dependencies
echo.
echo Installing additional dependencies for API server...
pip install fastapi uvicorn pyjwt python-multipart python-dotenv

echo.
echo Dependencies installed successfully!
echo To run the API server, execute: python api.py

:: Interactive API key setup
echo.
echo Setting up environment file...
set /p has_key="Do you have a Google Gemini API key? (y/n): "

if /i "%has_key%"=="y" (
    set /p api_key="Please enter your Google Gemini API key: "
) else (
    echo You'll need to get a Google Gemini API key to use this application.
    echo Follow these steps:
    echo 1. Visit https://aistudio.google.com/ and sign in with your Google account
    echo 2. Click on 'Get API key' in the navigation menu
    echo 3. Create a new API key (or use an existing one)
    echo 4. Copy the API key
    echo.
    
    set /p api_key="Once you have your API key, please enter it: "
)

:: Create .env file
echo.
echo Creating .env file...
echo GEMINI_API_KEY=%api_key%> .env
echo SQLITE_DB_PATH=hotel.db>> .env
echo JWT_SECRET_KEY=supersecretkey>> .env

:: Run database setup
echo.
echo Setting up the database...
python setup.py

echo.
echo Setup complete!
echo To run the application, make sure the virtual environment is activated:
echo venv\Scripts\activate.bat
echo.
echo To run the API server:
echo python api.py
echo.
echo Press any key to exit...
pause > nul