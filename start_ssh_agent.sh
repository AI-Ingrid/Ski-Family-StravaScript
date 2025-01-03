#!/bin/bash

# Check if the .env file path is provided
if [ -z "$1" ]; then
  echo "Usage: $0 path_to_env_file"
  exit 1
fi

# Source the .env file to load environment variables
source "$1"

# Use the environment variables
SSH_AGENT_ENV="${SSH_KEY_PATH}/ssh_agent_env"
SSH_KEY="${SSH_KEY_PATH}/id_rsa"

# Start the SSH agent
eval "$(ssh-agent -s)"

# Add the SSH key
ssh-add "$SSH_KEY"

# Save the SSH agent information
echo "export SSH_AUTH_SOCK=$SSH_AUTH_SOCK" > "$SSH_AGENT_ENV"
echo "export SSH_AGENT_PID=$SSH_AGENT_PID" >> "$SSH_AGENT_ENV"
