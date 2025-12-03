#!/usr/bin/env bash

# move to the directory where start.sh is located
cd "$(dirname "$(readlink -f "$0")")"


# activate virtual environment
source venv/Scripts/activate

# run the app
uvicorn main:app --reload
