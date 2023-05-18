#!/bin/bash

# Define colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Spinner function
spinner()
{
    local pid=$1
    local delay=0.75
    local spinstr='|/-\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

# Clear the terminal
clear

# Print a welcome message
echo -e "${GREEN}\nWelcome to LambdaTunnel fast_setup.sh script!${NC}"
echo "This script enables you to run Stable Diffusion Automatic1111 webui on a rented H100 but use it locally from Mac or iPad."

# Print a warning message
echo -e "${RED}\nWARNING: Please exercise caution when executing scripts from the internet. For more information, visit https://github.com/adriangalilea/LambdaTunnel/blob/main/README.md${NC}"

# Ask for the server's IP address and confirm user's acceptance of risks
echo -e "\nBy entering your SSH server's IP address and continuing, you acknowledge the risks and agree to use the software as-is. I am not responsible for any potential issues."
read -p "\nEnter your SSH server's IP address to continue: " server_ip

# Check if the user wants to quit
if [ -z "$server_ip" ]; then
  echo -e "\nEnter your SSH server's IP address to continue: \c"
  read server_ip
  exit 0
fi

# Ping the server
echo -e "\n${GREEN}Pinging the server...${NC}"
ping -c 1 $server_ip > /dev/null &
spinner $!
if [ $? -ne 0 ]; then
    echo -e "\r${RED}The server at $server_ip is not responding. Please check the server IP address and try again.${NC}"
    exit 1
fi

echo -e "\r${GREEN}Server at $server_ip is reachable.${NC}\n"

# Check if an SSH tunnel already exists
existing_tunnel_pid=$(lsof -ti :7860)

if [[ -z "$existing_tunnel_pid" ]]; then
  # Create an SSH tunnel
  echo -e "${GREEN}Setting up SSH tunnel...${NC}"
  ssh -N -L 7860:localhost:7860 ubuntu@$server_ip > /dev/null &
  spinner $!
  echo -e "\r${GREEN}SSH tunnel is up.${NC}\n"
else
  echo -e "\r${GREEN}SSH tunnel is already up. (PID: $existing_tunnel_pid)${NC}\n"
fi


# Set up tmux session
echo -e "${GREEN}Setting up tmux session on remote instance...${NC}"
i=0
ssh -t ubuntu@$server_ip "tmux has-session -t stable_webui" 2>/dev/null
if [ $? -eq 0 ]; then
  echo -e "${GREEN}tmux session is already running.${NC}\n"
else
  ssh -t ubuntu@$server_ip "tmux new-session -d -s stable_webui 'bash <(wget -qO- https://raw.githubusercontent.com/AUTOMATIC1111/stable-diffusion-webui/master/webui.sh)'" &
  while [ $? -ne 0 ]; do
    i=$(((i + 1) % 4))
    printf "\r${RED}Setting up tmux session... ${spin:$i:1}${NC}"
    sleep 1
    ssh -t ubuntu@$server_ip "tmux new-session -d -s stable_webui 'bash <(wget -qO- https://raw.githubusercontent.com/AUTOMATIC1111/stable-diffusion-webui/master/webui.sh)'" &
  done
  echo -e "\r${GREEN}tmux session is up.${NC}\n"
fi

# Check localhost on port 7860
echo -e "${GREEN}Checking localhost on port 7860...${NC}"

while true; do
  # Send a request to 127.0.0.1:7860 and capture the output
  page_content=$(curl -s http://127.0.0.1:7860)

  # If the output is not empty (which means the server is responding), break the loop
  if [[ ! -z "$page_content" ]]; then
    echo -e "\r${GREEN}localhost:7860 is serving.${NC}\n"
    break
  else
    printf "\r${RED}localhost:7860 is not serving yet. Retrying...${NC}"
    sleep 5
  fi
done

# We open up a tab
open "http://127.0.0.1:7860"

while true; do
  # Clear the terminal and print options
  clear
  echo -e "${GREEN}http://127.0.0.1:7860 is live.${NC}\n"
  echo -e "\n${GREEN}Options:${NC}"
  echo "1. [Optional] Install sshfs to allow accessing the remote server through Finder."
  echo "2. [Optional] Mount the SSH server. (This allows you to access the remote server through Finder.)"
  echo "3. View output of remote tmux session."
  echo "4. Exit."
  read -p "Enter the number of the option you wish to proceed with: " option

  if [ "$option" == "1" ]; then
    echo -e "\n${GREEN}Installing sshfs to allow accessing the remote server through Finder...${NC}"
    brew install --cask macfuse
    curl -LO https://github.com/osxfuse/sshfs/releases/download/osxfuse-sshfs-2.5.0/sshfs-2.5.0.pkg && sudo installer -pkg sshfs-2.5.0.pkg -target /
  elif [ "$option" == "2" ]; then
    echo -e "\n${GREEN}Attempting to mount the SSH server...${NC}"
    mkdir -p ~/mount_point && sshfs -o allow_other,defer_permissions ubuntu@$server_ip: ~/mount_point
  elif [ "$option" == "3" ]; then
    if ! command -v watch &>/dev/null; then
      echo "The 'watch' command is required but it's not installed."
      read -p "Do you wish to install 'watch' now? (y/n) " confirm
      if [ "$confirm" == "y" ]; then
        brew install watch
      else
        echo "Cannot proceed without 'watch'. Please install it and try again."
        continue
      fi
    fi
    echo -e "\n${GREEN}Monitoring the output of the remote tmux session. Press 'Ctrl+C' to stop.${NC}"
    watch -n 1 "echo -e '\n${RED}Press Ctrl+C to stop watching${NC}'; ssh -t ubuntu@$server_ip 'tmux capture-pane -p -t stable_webui; tmux show-buffer' 2> /dev/null"
  elif [ "$option" == "4" ]; then
    echo -e "\n${RED}WARNING: You MUST manually shutdown the instance in the Lambda Cloud web interface or you'll continue to be charged by the hour. Opening the web interface now...${NC}"
    # Terminate the SSH tunnel
    pkill -f "ssh -N -L 7860:localhost:7860 ubuntu@$server_ip"
    # Open Lambda Cloud web interface in the default browser
    open "https://lambdalabs.com/cloud/dashboard/instances"
    break
  else
    echo -e "\n${RED}Invalid option. Please try again.${NC}"
  fi
done

echo -e "\n${GREEN}Thank you for using LambdaTunnel! Goodbye!${NC}"