#!/usr/bin/env python3
"""
Unit tests for Castroix application
Tests core functionality without requiring GUI
"""
import unittest
import json
import os
from pathlib import Path
import sys

# Mock tkinter for testing in headless environment
class MockTk:
    def title(self, text): pass
    def geometry(self, size): pass
    def configure(self, **kwargs): pass
    def mainloop(self): pass

class MockWidget:
    def __init__(self, *args, **kwargs): pass
    def pack(self, **kwargs): pass
    def grid(self, **kwargs): pass
    def grid_rowconfigure(self, *args, **kwargs): pass
    def grid_columnconfigure(self, *args, **kwargs): pass
    def config(self, **kwargs): pass
    def bind(self, *args, **kwargs): pass

sys.modules['tkinter'] = type(sys)('tkinter')
sys.modules['tkinter'].Tk = MockTk
sys.modules['tkinter'].Label = MockWidget
sys.modules['tkinter'].Button = MockWidget
sys.modules['tkinter'].Frame = MockWidget
sys.modules['tkinter'].ttk = type(sys)('ttk')
sys.modules['tkinter'].messagebox = type(sys)('messagebox')
sys.modules['tkinter'].messagebox.showwarning = lambda *args: None
sys.modules['tkinter'].messagebox.showerror = lambda *args: None

# Now we can import the application modules
from castroix import MediaService


class TestMediaService(unittest.TestCase):
    """Test MediaService class"""
    
    def test_media_service_creation(self):
        """Test creating a MediaService instance"""
        service = MediaService(
            name="Test Service",
            url="https://example.com",
            icon_color="#ff0000"
        )
        self.assertEqual(service.name, "Test Service")
        self.assertEqual(service.url, "https://example.com")
        self.assertEqual(service.icon_color, "#ff0000")
        self.assertIsNone(service.command)
    
    def test_media_service_with_command(self):
        """Test creating a MediaService with command"""
        service = MediaService(
            name="Test App",
            command="test-app",
            icon_color="#00ff00"
        )
        self.assertEqual(service.name, "Test App")
        self.assertEqual(service.command, "test-app")
        self.assertIsNone(service.url)


class TestConfiguration(unittest.TestCase):
    """Test configuration handling"""
    
    def setUp(self):
        """Setup test configuration"""
        self.test_config_path = Path("/tmp/test_config.json")
        self.test_config = {
            "services": {
                "test": {
                    "name": "Test Service",
                    "url": "https://test.com",
                    "command": None,
                    "icon_color": "#123456"
                }
            }
        }
    
    def tearDown(self):
        """Cleanup test files"""
        if self.test_config_path.exists():
            self.test_config_path.unlink()
    
    def test_config_structure(self):
        """Test that config has correct structure"""
        config_path = Path(__file__).parent / "config.json"
        self.assertTrue(config_path.exists(), "config.json should exist")
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        self.assertIn("services", config)
        self.assertIn("plex", config["services"])
        self.assertIn("jellyfin", config["services"])
        self.assertIn("netflix", config["services"])
        self.assertIn("disneyplus", config["services"])
    
    def test_service_config_fields(self):
        """Test that each service has required fields"""
        config_path = Path(__file__).parent / "config.json"
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        for service_key, service_config in config["services"].items():
            self.assertIn("name", service_config, 
                f"{service_key} should have 'name' field")
            self.assertIn("icon_color", service_config,
                f"{service_key} should have 'icon_color' field")
            # Should have either url or command
            self.assertTrue(
                "url" in service_config or "command" in service_config,
                f"{service_key} should have 'url' or 'command' field"
            )


class TestColorUtils(unittest.TestCase):
    """Test color utility functions"""
    
    def test_hex_color_format(self):
        """Test that colors in config are valid hex codes"""
        config_path = Path(__file__).parent / "config.json"
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        for service_key, service_config in config["services"].items():
            color = service_config.get("icon_color")
            if color:
                # Should start with # and have 6 hex digits
                self.assertTrue(color.startswith("#"), 
                    f"{service_key} color should start with #")
                self.assertEqual(len(color), 7,
                    f"{service_key} color should be #RRGGBB format")
                # Check if valid hex
                try:
                    int(color[1:], 16)
                except ValueError:
                    self.fail(f"{service_key} color is not valid hex")


class TestErrorHandling(unittest.TestCase):
    """Test error handling"""
    
    def test_tkinter_error_message(self):
        """Test that helpful error message is shown when tkinter is missing"""
        import subprocess
        import sys
        
        # Create a test script that simulates missing tkinter
        test_script = '''
import sys
# Block tkinter import
sys.modules['tkinter'] = None

# Now try to import castroix - should show error message
try:
    import castroix
except SystemExit as e:
    # Expected - the module should exit with code 1
    sys.exit(e.code)
'''
        
        # Run the test script
        result = subprocess.run(
            [sys.executable, '-c', test_script],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True
        )
        
        # Should exit with code 1
        self.assertEqual(result.returncode, 1, 
            "Script should exit with code 1 when tkinter is missing")
        
        # Should contain helpful error message
        self.assertIn("tkinter is not installed", result.stdout.lower(),
            "Error message should mention tkinter is not installed")
        self.assertIn("apt-get", result.stdout.lower(),
            "Error message should include installation instructions")


def run_tests():
    """Run all tests"""
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestMediaService))
    suite.addTests(loader.loadTestsFromTestCase(TestConfiguration))
    suite.addTests(loader.loadTestsFromTestCase(TestColorUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
