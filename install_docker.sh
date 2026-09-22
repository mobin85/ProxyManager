#!/bin/bash

# Exit on any error
set -e

echo "Starting Docker and Docker Compose installation..."

# Update package manager and install curl if not present
sudo apt-get update
sudo apt-get install -y curl

# Download and run Docker's official convenience script
# This script automatically detects the Debian-based distro and installs the correct packages
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# The convenience script typically installs the docker-compose-plugin (accessed via `docker compose`),
# but we explicitly ensure it is installed just in case.
sudo apt-get update
sudo apt-get install -y docker-compose-plugin

# Enable and start Docker services
sudo systemctl enable docker
sudo systemctl start docker

# Clean up the downloaded script
rm get-docker.sh

echo "========================================="
echo "Installation Completed Successfully!"
echo "========================================="

# Verify versions
docker --version
docker compose version

echo "========================================="
echo "Note: If you want to run Docker without 'sudo', please run the following command:"
echo "sudo usermod -aG docker \$USER"
echo "Then, log out and log back in for the changes to take effect."
