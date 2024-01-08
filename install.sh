#!/bin/bash

# Color codes for banner
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Function to check if a command is available
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Python modules
install_python_modules() {
    echo -e "${YELLOW}Installing Python modules...${RESET}"
    pip install -r requirements.txt
    echo -e "${GREEN}Python modules installed successfully.${RESET}"
}

# Function to install gau
install_gau() {
    if ! command_exists "gau"; then
        echo -e "${YELLOW}Installing gau...${RESET}"
        go get -u github.com/lc/gau
        echo -e "${GREEN}gau installed successfully.${RESET}"
    else
        echo -e "${GREEN}gau is already installed.${RESET}"
    fi
}

# Function to install Tor
install_tor() {
    if ! command_exists "tor"; then
        echo -e "${YELLOW}Installing Tor...${RESET}"
        sudo apt-get update
        sudo apt-get install tor
        echo -e "${GREEN}Tor installed successfully.${RESET}"
    else
        echo -e "${GREEN}Tor is already installed.${RESET}"
    fi
}

# Function to display banner
display_banner() {
    echo -e "${BLUE}██╗  ██╗██╗███████╗██╗  ██╗"
    echo -e "${CYAN}██║  ██║██║██╔════╝╚██╗██╔╝"
    echo -e "${PURPLE}███████║██║███████╗ ╚███╔╝ "
    echo -e "${RED}██╔══██║██║╚════██║ ██╔██╗ "
    echo -e "${YELLOW}██║  ██║██║███████║██╔╝ ██╗"
    echo -e "${GREEN}╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝${RESET}"
    echo -e "${GREEN}        XSS Scanner by TRHACKNON${RESET}"
}

# Main script
clear
display_banner

# Prompt user to install Python modules
read -p "Do you want to install Python modules? (y/n): " install_python
if [ "$install_python" == "y" ]; then
    install_python_modules
fi

# Prompt user to install gau
read -p "Do you want to install gau? (y/n): " install_gau_input
if [ "$install_gau_input" == "y" ]; then
    install_gau
fi

# Prompt user to install Tor
read -p "Do you want to install Tor? (y/n): " install_tor_input
if [ "$install_tor_input" == "y" ]; then
    install_tor
fi

# Prompt user to launch main.py
read -p "Do you want to launch main.py? (y/n): " launch_main_input
if [ "$launch_main_input" == "y" ]; then
    python3 main.py
fi