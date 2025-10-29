#!/bin/bash

# WildOps Setup Script
# This script helps set up the WildOps project for the first time

set -e  # Exit on error

echo "======================================"
echo "WildOps Setup Script"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed. Please install Python 3.10 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓${NC} Found Python $PYTHON_VERSION"

# Check Python version (should be 3.10+)
REQUIRED_VERSION="3.10"
if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${YELLOW}Warning: Python $PYTHON_VERSION detected. Python 3.10+ is recommended.${NC}"
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists. Skipping creation.${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies..."
echo -e "${YELLOW}This may take a few minutes...${NC}"
pip install -r requirements.txt

# Create .env file from template if it doesn't exist
echo ""
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo -e "${GREEN}✓${NC} Created .env file"
    echo -e "${YELLOW}⚠ IMPORTANT: Edit .env file and add your API keys and configuration${NC}"
else
    echo -e "${YELLOW}.env file already exists. Skipping creation.${NC}"
fi

# Generate a new SECRET_KEY
echo ""
echo "Generating Django SECRET_KEY..."
cd WildOpsProject
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
cd ..
echo -e "${GREEN}✓${NC} Generated SECRET_KEY"
echo ""
echo -e "${YELLOW}Add this to your .env file:${NC}"
echo "SECRET_KEY=$SECRET_KEY"
echo ""

# Run migrations
echo ""
echo "Running database migrations..."
cd WildOpsProject
python manage.py migrate
echo -e "${GREEN}✓${NC} Database migrations complete"

# Create user groups
echo ""
echo "Creating user groups and permissions..."
python manage.py create_groups
echo -e "${GREEN}✓${NC} User groups created"

# Ask to create superuser
echo ""
read -p "Do you want to create a superuser now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
    echo -e "${GREEN}✓${NC} Superuser created"
else
    echo -e "${YELLOW}You can create a superuser later with: python manage.py createsuperuser${NC}"
fi

cd ..

# Create necessary directories
echo ""
echo "Creating necessary directories..."
mkdir -p WildOpsProject/media
mkdir -p WildOpsProject/WildProcedures/static/WildProcedures/pdfs
mkdir -p WildOpsProject/scripts/logs
echo -e "${GREEN}✓${NC} Directories created"

# Make scripts executable
echo ""
echo "Making scripts executable..."
chmod +x WildOpsProject/scripts/run_update_activation_state.sh 2>/dev/null || true
echo -e "${GREEN}✓${NC} Scripts configured"

echo ""
echo "======================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Edit the .env file and add your API keys:"
echo "   - WEATHERAPI_KEY (get from https://www.weatherapi.com/)"
echo "   - RAPIDAPI_KEY (get from https://rapidapi.com/)"
echo "   - SECRET_KEY (use the one generated above)"
echo ""
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Navigate to the project directory:"
echo "   cd WildOpsProject"
echo ""
echo "4. Start the development server:"
echo "   python manage.py runserver"
echo ""
echo "5. Open your browser and go to:"
echo "   http://127.0.0.1:8000/"
echo ""
echo "6. Access the admin panel at:"
echo "   http://127.0.0.1:8000/admin/"
echo ""
echo -e "${YELLOW}For production deployment, see README.md${NC}"
echo ""
