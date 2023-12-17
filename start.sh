#!/bin/bash

# Source the .env file to set environment variables
if [ -f "/project/.env" ]; then
    export $(cat .env | xargs)

fi

# Run the main command (e.g., python run.py)
python run.py