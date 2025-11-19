# Castroix Setup Script for Windows (PowerShell)
# Automatically detects Node.js and NPM, and sets up the application

# Function to print colored output
function Write-Info {
    param($Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Success {
    param($Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param($Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param($Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Function to check if a command exists
function Test-Command {
    param($Command)
    try {
        if (Get-Command $Command -ErrorAction Stop) {
            return $true
        }
    }
    catch {
        return $false
    }
    return $false
}

# Function to check Node.js installation
function Test-NodeJS {
    Write-Info "Checking for Node.js installation..."
    
    if (Test-Command "node") {
        $nodeVersion = node --version
        Write-Success "Node.js is installed: $nodeVersion"
        
        # Check if version is >= 16
        $versionNumber = $nodeVersion -replace 'v', '' -split '\.' | Select-Object -First 1
        if ([int]$versionNumber -lt 16) {
            Write-Warning "Node.js version is less than 16.x. Version 16.x or higher is recommended."
            return $false
        }
        return $true
    }
    else {
        Write-Warning "Node.js is not installed."
        return $false
    }
}

# Function to check npm installation
function Test-NPM {
    Write-Info "Checking for npm installation..."
    
    if (Test-Command "npm") {
        $npmVersion = npm --version
        Write-Success "npm is installed: $npmVersion"
        return $true
    }
    else {
        Write-Warning "npm is not installed."
        return $false
    }
}

# Function to install Node.js using winget (Windows 10+)
function Install-NodeJS {
    Write-Info "Attempting to install Node.js..."
    
    # Check if winget is available (Windows 10 1809+ / Windows 11)
    if (Test-Command "winget") {
        Write-Info "Installing Node.js via winget..."
        try {
            winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
            Write-Success "Node.js installation completed!"
            Write-Warning "Please close and reopen PowerShell/Terminal, then run this script again."
            return $true
        }
        catch {
            Write-Error "Failed to install Node.js via winget."
            return $false
        }
    }
    # Check if chocolatey is available
    elseif (Test-Command "choco") {
        Write-Info "Installing Node.js via Chocolatey..."
        try {
            choco install nodejs-lts -y
            Write-Success "Node.js installation completed!"
            Write-Warning "Please close and reopen PowerShell/Terminal, then run this script again."
            return $true
        }
        catch {
            Write-Error "Failed to install Node.js via Chocolatey."
            return $false
        }
    }
    else {
        Write-Warning "No package manager found (winget or chocolatey)."
        return $false
    }
}

# Function to install npm dependencies
function Install-Dependencies {
    Write-Info "Installing npm dependencies..."
    
    if (Test-Path "package.json") {
        npm install
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Dependencies installed successfully!"
            return $true
        }
        else {
            Write-Error "Failed to install dependencies."
            return $false
        }
    }
    else {
        Write-Error "package.json not found. Are you in the correct directory?"
        return $false
    }
}

# Function to setup configuration
function Initialize-Config {
    if (-not (Test-Path "config.json")) {
        if (Test-Path "config.json.sample") {
            Write-Info "Creating config.json from config.json.sample..."
            Copy-Item "config.json.sample" "config.json"
            Write-Success "config.json created successfully!"
        }
        else {
            Write-Warning "config.json.sample not found. You may need to create config.json manually."
        }
    }
    else {
        Write-Info "config.json already exists, skipping creation."
    }
}

# Main script execution
Write-Host "========================================" -ForegroundColor White
Write-Host "      Castroix Setup Script" -ForegroundColor White
Write-Host "========================================" -ForegroundColor White
Write-Host ""

Write-Success "Detected: Windows"
Write-Host ""

# Check for Node.js and npm
$nodeInstalled = Test-NodeJS
Write-Host ""
$npmInstalled = Test-NPM
Write-Host ""

# Install Node.js if not installed
if (-not $nodeInstalled -or -not $npmInstalled) {
    Write-Warning "Node.js and/or npm are not installed or need updating."
    $install = Read-Host "Would you like to attempt automatic installation? (Y/N)"
    
    if ($install -eq "Y" -or $install -eq "y") {
        $success = Install-NodeJS
        
        if ($success) {
            Write-Host ""
            Write-Info "Please restart PowerShell and run this script again to complete setup."
            Read-Host "Press Enter to exit"
            exit 0
        }
    }
    
    # Manual installation instructions
    Write-Host ""
    Write-Error "Node.js is required to run Castroix."
    Write-Info "Please download and install Node.js manually from: https://nodejs.org/"
    Write-Host ""
    $openBrowser = Read-Host "Would you like to open the Node.js download page? (Y/N)"
    if ($openBrowser -eq "Y" -or $openBrowser -eq "y") {
        Start-Process "https://nodejs.org/"
    }
    Write-Host ""
    Write-Info "After installation, restart PowerShell and run this script again."
    Read-Host "Press Enter to exit"
    exit 1
}

# Install dependencies
$depsInstalled = Install-Dependencies
Write-Host ""

if (-not $depsInstalled) {
    Read-Host "Press Enter to exit"
    exit 1
}

# Setup configuration
Initialize-Config
Write-Host ""

Write-Success "Setup completed successfully!"
Write-Host ""

# Ask to launch
$launch = Read-Host "Would you like to launch Castroix now? (Y/N)"
if ($launch -eq "Y" -or $launch -eq "y") {
    Write-Info "Launching Castroix..."
    npm start
}
else {
    Write-Info "You can launch Castroix later by running: npm start"
}

Write-Host ""
Read-Host "Press Enter to exit"
