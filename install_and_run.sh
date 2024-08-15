#!/bin/bash

# Function to install Python3
install_python3() {
    echo "Installing Python3..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if ! command -v brew &> /dev/null; then
            echo "Homebrew not found. Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python
    else
        # Linux
        echo "Installing Python3 on Linux..."
        echo "$USER_PASSWORD" | sudo -S apt update
        echo "$USER_PASSWORD" | sudo -S apt install -y python3
    fi
}

# Function to install pip3
install_pip3() {
    echo "Installing pip3..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install pip3
    else
        # Linux
        echo "Installing pip3 on Linux..."
        echo "$USER_PASSWORD" | sudo -S apt install -y python3-pip
    fi
}

# Function to install Flask
install_flask() {
    echo "Installing Flask..."
    pip3 install Flask
}

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    install_python3
fi

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null; then
    install_pip3
fi

# Check if Flask is installed
if ! python3 -c "import flask" &> /dev/null; then
    install_flask
fi

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run the Flask application
export FLASK_APP=app.py
flask run

# Deactivate the virtual environment
deactivate
