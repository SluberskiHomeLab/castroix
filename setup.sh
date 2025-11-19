#!/bin/bash

# Castroix Setup Script
# Automatically detects OS, checks/installs Node.js and NPM, and sets up the application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to detect operating system
detect_os() {
    print_info "Detecting operating system..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="Linux"
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            DISTRO=$ID
            print_success "Detected: Linux ($NAME)"
        else
            DISTRO="unknown"
            print_success "Detected: Linux (Unknown distribution)"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macOS"
        print_success "Detected: macOS"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        OS="Windows"
        print_success "Detected: Windows (via $OSTYPE)"
    else
        OS="Unknown"
        print_warning "Unknown operating system: $OSTYPE"
    fi
}

# Function to check if Node.js is installed
check_nodejs() {
    print_info "Checking for Node.js installation..."
    
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_success "Node.js is installed: $NODE_VERSION"
        
        # Check if version is >= 16
        NODE_MAJOR=$(echo $NODE_VERSION | cut -d'v' -f2 | cut -d'.' -f1)
        if [ "$NODE_MAJOR" -lt 16 ]; then
            print_warning "Node.js version is less than 16.x. Version 16.x or higher is recommended."
            return 1
        fi
        return 0
    else
        print_warning "Node.js is not installed."
        return 1
    fi
}

# Function to check if npm is installed
check_npm() {
    print_info "Checking for npm installation..."
    
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        print_success "npm is installed: $NPM_VERSION"
        return 0
    else
        print_warning "npm is not installed."
        return 1
    fi
}

# Function to install Node.js on Linux
install_nodejs_linux() {
    print_info "Installing Node.js on Linux ($DISTRO)..."
    
    case "$DISTRO" in
        ubuntu|debian)
            print_info "Installing Node.js via NodeSource repository..."
            if command -v curl &> /dev/null; then
                curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
                sudo apt-get install -y nodejs
            else
                print_error "curl is not installed. Please install curl first: sudo apt-get install curl"
                exit 1
            fi
            ;;
        fedora|rhel|centos)
            print_info "Installing Node.js via NodeSource repository..."
            if command -v curl &> /dev/null; then
                curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
                sudo dnf install -y nodejs
            else
                print_error "curl is not installed. Please install curl first: sudo dnf install curl"
                exit 1
            fi
            ;;
        arch|manjaro)
            print_info "Installing Node.js via pacman..."
            sudo pacman -S --noconfirm nodejs npm
            ;;
        *)
            print_error "Automatic installation not supported for your distribution ($DISTRO)."
            print_info "Please install Node.js manually from: https://nodejs.org/"
            print_info "Or use your distribution's package manager."
            exit 1
            ;;
    esac
}

# Function to install Node.js on macOS
install_nodejs_macos() {
    print_info "Installing Node.js on macOS..."
    
    if command -v brew &> /dev/null; then
        print_info "Installing Node.js via Homebrew..."
        brew install node
    else
        print_error "Homebrew is not installed."
        print_info "Please install Homebrew first: https://brew.sh/"
        print_info "Or download Node.js manually from: https://nodejs.org/"
        exit 1
    fi
}

# Function to install Node.js on Windows (Git Bash/MSYS)
install_nodejs_windows() {
    print_error "Automatic installation on Windows via bash is not fully supported."
    print_info "Please download and install Node.js from: https://nodejs.org/"
    print_info "After installation, restart this script."
    exit 1
}

# Function to install Node.js based on OS
install_nodejs() {
    case "$OS" in
        Linux)
            install_nodejs_linux
            ;;
        macOS)
            install_nodejs_macos
            ;;
        Windows)
            install_nodejs_windows
            ;;
        *)
            print_error "Cannot install Node.js on unknown operating system."
            exit 1
            ;;
    esac
    
    # Verify installation
    if check_nodejs && check_npm; then
        print_success "Node.js and npm have been installed successfully!"
    else
        print_error "Installation verification failed. Please install Node.js manually."
        exit 1
    fi
}

# Function to install npm dependencies
install_dependencies() {
    print_info "Installing npm dependencies..."
    
    if [ -f "package.json" ]; then
        npm install
        print_success "Dependencies installed successfully!"
    else
        print_error "package.json not found. Are you in the correct directory?"
        exit 1
    fi
}

# Function to create config.json if it doesn't exist
setup_config() {
    if [ ! -f "config.json" ]; then
        if [ -f "config.json.sample" ]; then
            print_info "Creating config.json from config.json.sample..."
            cp config.json.sample config.json
            print_success "config.json created successfully!"
        else
            print_warning "config.json.sample not found. You may need to create config.json manually."
        fi
    else
        print_info "config.json already exists, skipping creation."
    fi
}

# Function to ask if user wants to launch the app
ask_launch() {
    echo ""
    read -p "Would you like to launch Castroix now? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Launching Castroix..."
        npm start
    else
        print_info "You can launch Castroix later by running: npm start"
    fi
}

# Main script execution
main() {
    echo "========================================"
    echo "      Castroix Setup Script"
    echo "========================================"
    echo ""
    
    # Detect operating system
    detect_os
    echo ""
    
    # Check for Node.js and npm
    NODE_INSTALLED=false
    if check_nodejs && check_npm; then
        NODE_INSTALLED=true
    fi
    echo ""
    
    # Install Node.js if not installed
    if [ "$NODE_INSTALLED" = false ]; then
        print_warning "Node.js and/or npm are not installed or need updating."
        read -p "Would you like to install Node.js now? (y/n): " -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            install_nodejs
            echo ""
        else
            print_error "Node.js is required to run Castroix."
            print_info "Please install Node.js manually from: https://nodejs.org/"
            exit 1
        fi
    fi
    
    # Install dependencies
    install_dependencies
    echo ""
    
    # Setup configuration
    setup_config
    echo ""
    
    print_success "Setup completed successfully!"
    echo ""
    
    # Ask to launch
    ask_launch
}

# Run main function
main
