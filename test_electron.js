/**
 * Basic tests for Electron version of Castroix
 * Validates configuration and basic functionality
 */

const fs = require('fs');
const path = require('path');

// Test configuration loading
function testConfigLoading() {
  console.log('Testing configuration loading...');
  
  const configPath = path.join(__dirname, 'config.json');
  const sampleConfigPath = path.join(__dirname, 'config.json.sample');
  
  if (!fs.existsSync(configPath) && !fs.existsSync(sampleConfigPath)) {
    console.error('❌ No config.json or config.json.sample found');
    return false;
  }
  
  try {
    const configFile = fs.existsSync(configPath) ? configPath : sampleConfigPath;
    const config = JSON.parse(fs.readFileSync(configFile, 'utf-8'));
    
    if (!config.services) {
      console.error('❌ Config missing services object');
      return false;
    }
    
    console.log('✅ Configuration loaded successfully');
    return true;
  } catch (error) {
    console.error('❌ Error loading config:', error.message);
    return false;
  }
}

// Test required files exist
function testRequiredFiles() {
  console.log('Testing required files...');
  
  const requiredFiles = [
    'main.js',
    'preload.js',
    'index.html',
    'styles.css',
    'renderer.js',
    'package.json'
  ];
  
  let allExist = true;
  
  for (const file of requiredFiles) {
    const filePath = path.join(__dirname, file);
    if (!fs.existsSync(filePath)) {
      console.error(`❌ Missing required file: ${file}`);
      allExist = false;
    }
  }
  
  if (allExist) {
    console.log('✅ All required files exist');
  }
  
  return allExist;
}

// Test package.json structure
function testPackageJson() {
  console.log('Testing package.json...');
  
  try {
    const packageJson = JSON.parse(fs.readFileSync(path.join(__dirname, 'package.json'), 'utf-8'));
    
    if (!packageJson.main) {
      console.error('❌ package.json missing main entry');
      return false;
    }
    
    if (!packageJson.dependencies || !packageJson.dependencies.electron) {
      console.error('❌ package.json missing electron dependency');
      return false;
    }
    
    if (!packageJson.dependencies['electron-store']) {
      console.error('❌ package.json missing electron-store dependency');
      return false;
    }
    
    console.log('✅ package.json is valid');
    return true;
  } catch (error) {
    console.error('❌ Error reading package.json:', error.message);
    return false;
  }
}

// Test HTML structure
function testHtmlStructure() {
  console.log('Testing HTML structure...');
  
  try {
    const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf-8');
    
    const requiredElements = [
      'services-grid',
      'credentials-modal',
      'home-view'
    ];
    
    let allFound = true;
    for (const elementId of requiredElements) {
      if (!html.includes(`id="${elementId}"`)) {
        console.error(`❌ HTML missing element with id: ${elementId}`);
        allFound = false;
      }
    }
    
    if (allFound) {
      console.log('✅ HTML structure is valid');
    }
    
    return allFound;
  } catch (error) {
    console.error('❌ Error reading HTML:', error.message);
    return false;
  }
}

// Test service configuration
function testServiceConfig() {
  console.log('Testing service configurations...');
  
  try {
    const configPath = path.join(__dirname, 'config.json');
    const sampleConfigPath = path.join(__dirname, 'config.json.sample');
    const configFile = fs.existsSync(configPath) ? configPath : sampleConfigPath;
    
    const config = JSON.parse(fs.readFileSync(configFile, 'utf-8'));
    const services = config.services;
    
    if (Object.keys(services).length === 0) {
      console.error('❌ No services configured');
      return false;
    }
    
    let allValid = true;
    for (const [key, service] of Object.entries(services)) {
      if (!service.name) {
        console.error(`❌ Service ${key} missing name`);
        allValid = false;
      }
      
      if (!service.icon_color) {
        console.error(`❌ Service ${key} missing icon_color`);
        allValid = false;
      }
      
      if (!service.url && !service.command) {
        console.error(`❌ Service ${key} missing both url and command`);
        allValid = false;
      }
    }
    
    if (allValid) {
      console.log(`✅ All ${Object.keys(services).length} services are valid`);
    }
    
    return allValid;
  } catch (error) {
    console.error('❌ Error testing service config:', error.message);
    return false;
  }
}

// Test keyboard shortcut handling in renderer.js
function testKeyboardShortcuts() {
  console.log('Testing keyboard shortcut implementation...');
  
  try {
    const rendererJs = fs.readFileSync(path.join(__dirname, 'renderer.js'), 'utf-8');
    
    // Check that Ctrl+Q handler exists with case-insensitive comparison
    if (!rendererJs.includes("e.ctrlKey && e.key.toLowerCase() === 'q'")) {
      console.error('❌ Ctrl+Q handler not found or not case-insensitive in renderer.js');
      return false;
    }
    
    // Check that it closes embedded browser when home-view is hidden
    if (!rendererJs.includes("document.getElementById('home-view').style.display === 'none'")) {
      console.error('❌ Ctrl+Q does not check for embedded browser state');
      return false;
    }
    
    // Check that it calls closeBrowser
    if (!rendererJs.includes('window.castroix.closeBrowser()')) {
      console.error('❌ Ctrl+Q does not call closeBrowser for embedded browser');
      return false;
    }
    
    // Check that Ctrl+S handler exists with case-insensitive comparison
    if (!rendererJs.includes("e.ctrlKey && e.key.toLowerCase() === 's'")) {
      console.error('❌ Ctrl+S handler not found or not case-insensitive in renderer.js');
      return false;
    }
    
    // Check that Escape handler exists
    if (!rendererJs.includes("e.key === 'Escape'") && !rendererJs.includes("case 'Escape':")) {
      console.error('❌ Escape key handler not found in renderer.js');
      return false;
    }
    
    console.log('✅ Keyboard shortcuts are properly implemented');
    return true;
  } catch (error) {
    console.error('❌ Error testing keyboard shortcuts:', error.message);
    return false;
  }
}

// Run all tests
function runTests() {
  console.log('\n=== Castroix Electron Tests ===\n');
  
  const tests = [
    testRequiredFiles,
    testPackageJson,
    testConfigLoading,
    testServiceConfig,
    testHtmlStructure,
    testKeyboardShortcuts
  ];
  
  let passed = 0;
  let failed = 0;
  
  for (const test of tests) {
    console.log('');
    if (test()) {
      passed++;
    } else {
      failed++;
    }
  }
  
  console.log('\n=== Test Results ===');
  console.log(`✅ Passed: ${passed}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`Total: ${passed + failed}`);
  
  return failed === 0;
}

// Run tests if executed directly
if (require.main === module) {
  const success = runTests();
  process.exit(success ? 0 : 1);
}

module.exports = { runTests };
