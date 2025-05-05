#!/bin/bash

# Colors for better readability
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================${NC}"
echo -e "${GREEN}Hotel Management System Setup${NC}"
echo -e "${BLUE}=========================================${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3 and try again.${NC}"
    exit 1
fi

# Create virtual environment
echo -e "\n${YELLOW}Setting up virtual environment...${NC}"
python3 -m venv venv

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
pip install langchain langgraph langchain-openai python-dotenv

# Install required dependencies for API server
echo -e "\n${YELLOW}Installing additional dependencies for API server...${NC}"
pip install fastapi uvicorn pyjwt python-multipart python-dotenv

echo -e "\n${GREEN}Dependencies installed successfully!${NC}"
echo -e "${YELLOW}To run the API server, execute:${NC} ${BLUE}python api.py${NC}"

# Interactive API key setup
echo -e "\n${YELLOW}Setting up environment file...${NC}"
echo -e "${BLUE}Do you have a Google Gemini API key? (y/n)${NC}"
read -r has_key

if [ "$has_key" = "y" ]; then
    echo -e "${BLUE}Please enter your Google Gemini API key:${NC}"
    read -r api_key
else
    echo -e "${YELLOW}You'll need to get a Google Gemini API key to use this application.${NC}"
    echo -e "${YELLOW}Follow these steps:${NC}"
    echo -e "1. Visit ${BLUE}https://aistudio.google.com/${NC} and sign in with your Google account"
    echo -e "2. Click on 'Get API key' in the navigation menu"
    echo -e "3. Create a new API key (or use an existing one)"
    echo -e "4. Copy the API key\n"
    
    echo -e "${BLUE}Once you have your API key, please enter it:${NC}"
    read -r api_key
fi

# Create .env file
echo -e "\n${YELLOW}Creating .env file...${NC}"
echo "GEMINI_API_KEY=$api_key" > .env
echo "SQLITE_DB_PATH=hotel.db" >> .env

# Run database setup
echo -e "\n${YELLOW}Setting up the database...${NC}"
python3 setup.py

echo -e "\n${GREEN}Setup complete!${NC}"
echo -e "${YELLOW}To run the application, make sure the virtual environment is activated:${NC}"
echo -e "${BLUE}source venv/bin/activate${NC}"
echo -e "${YELLOW}Then you can use the agent in your Python code:${NC}"
echo -e "${BLUE}from agent import agent${NC}"
echo -e "${BLUE}response = agent.invoke({\"input\": \"List all vacant rooms.\"})${NC}"
echo -e "${BLUE}print(response[\"output\"])${NC}"

echo -e "\n${YELLOW}Would you like to run a quick test query? (y/n)${NC}"
read -r run_test

if [ "$run_test" = "y" ]; then
    echo -e "\n${YELLOW}Enter your query (e.g., 'List all vacant rooms'):${NC}"
    read -r query
    
    # Create a temporary Python script to run the query
    echo "from agent import agent" > temp_query.py
    echo "response = agent.invoke({\"messages\": [\"$query\"]})" >> temp_query.py
    echo "print(response[\"output\"])" >> temp_query.py
    
    # Run the query
    echo -e "\n${YELLOW}Running your query...${NC}"
    python3 temp_query.py
    
    # Clean up
    rm temp_query.py
fi

echo -e "\n${GREEN}Thank you for using the Hotel Management System!${NC}"