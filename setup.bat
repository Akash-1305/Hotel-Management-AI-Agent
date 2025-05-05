@echo off
setlocal EnableDelayedExpansion

echo =========================================
echo Hotel Management System Setup
echo =========================================

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

:: Interactive API key setup
echo.
echo Setting up environment file...
set /p has_key=Do you have a Google Gemini API key? (y/n): 

if /i "%has_key%"=="y" (
    set /p api_key=Please enter your Google Gemini API key: 
) else (
    echo You'll need to get a Google Gemini API key to use this application.
    echo Follow these steps:
    echo 1. Visit https://aistudio.google.com/ and sign in with your Google account
    echo 2. Click on 'Get API key' in the navigation menu
    echo 3. Create a new API key (or use an existing one)
    echo 4. Copy the API key
    echo.
    set /p api_key=Once you have your API key, please enter it: 
)

:: Create .env file
echo.
echo Creating .env file...
echo GEMINI_API_KEY=%api_key%> .env
echo SQLITE_DB_PATH=hotel.db>> .env

:: Run database setup
echo.
echo Setting up the database...
python setup.py

echo.
echo Setup complete!
echo To run the application, make sure the virtual environment is activated:
echo call venv\Scripts\activate.bat
echo Then you can use the agent in your Python code:
echo from agent import agent
echo response = agent.invoke({"input": "List all vacant rooms."})
echo print(response["output"])

echo.
set /p run_test=Would you like to run a quick test query? (y/n): 

if /i "%run_test%"=="y" (
    echo.
    set /p query=Enter your query (e.g., 'List all vacant rooms'): 
    
    :: Create a temporary Python script to run the query
    echo from agent import agent > temp_query.py
    echo response = agent.invoke({"input": "%query%"}) >> temp_query.py
    echo print(response["output"]) >> temp_query.py
    
    :: Run the query
    echo.
    echo Running your query...
    python temp_query.py
    
    :: Clean up
    del temp_query.py
)

echo.
echo Thank you for using the Hotel Management System!

:: Deactivate virtual environment if script was not sourced
call venv\Scripts\deactivate.bat