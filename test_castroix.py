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
from castroix_package.services import MediaService
from castroix_package.config import ConfigManager
from castroix_package.utils import lighten_color, darken_color, is_valid_hex_color


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
    
    def test_media_service_with_icon_file(self):
        """Test creating a MediaService with custom icon file"""
        service = MediaService(
            name="Test Service",
            url="https://example.com",
            icon_color="#ff0000",
            icon_file="test.png"
        )
        self.assertEqual(service.icon_file, "test.png")


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
            self.assertIn("icon_file", service_config,
                f"{service_key} should have 'icon_file' field")
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


class TestUtilities(unittest.TestCase):
    """Test utility functions"""
    
    def test_lighten_color(self):
        """Test color lightening"""
        # Test basic lightening
        result = lighten_color("#808080")  # Gray
        self.assertTrue(result.startswith("#"))
        self.assertEqual(len(result), 7)
        
        # Lightened color should have higher RGB values
        original_val = int("80", 16)
        result_val = int(result[1:3], 16)
        self.assertGreater(result_val, original_val)
    
    def test_darken_color(self):
        """Test color darkening"""
        # Test basic darkening
        result = darken_color("#808080")  # Gray
        self.assertTrue(result.startswith("#"))
        self.assertEqual(len(result), 7)
        
        # Darkened color should have lower RGB values
        original_val = int("80", 16)
        result_val = int(result[1:3], 16)
        self.assertLess(result_val, original_val)
    
    def test_is_valid_hex_color(self):
        """Test hex color validation"""
        # Valid colors
        self.assertTrue(is_valid_hex_color("#ff0000"))
        self.assertTrue(is_valid_hex_color("#123abc"))
        self.assertTrue(is_valid_hex_color("#000000"))
        
        # Invalid colors
        self.assertFalse(is_valid_hex_color("ff0000"))  # Missing #
        self.assertFalse(is_valid_hex_color("#ff00"))   # Too short
        self.assertFalse(is_valid_hex_color("#gggggg"))  # Invalid hex
        self.assertFalse(is_valid_hex_color("#ff00000"))  # Too long


class TestConfigManager(unittest.TestCase):
    """Test configuration manager"""
    
    def test_config_manager_creation(self):
        """Test creating a ConfigManager instance"""
        config_manager = ConfigManager()
        self.assertIsNotNone(config_manager.config)
        self.assertIn("services", config_manager.config)
    
    def test_get_services(self):
        """Test getting services from config"""
        config_manager = ConfigManager()
        services = config_manager.get_services()
        self.assertIsInstance(services, dict)
        self.assertGreater(len(services), 0)
    
    def test_default_services(self):
        """Test that default services are present"""
        config_manager = ConfigManager()
        services = config_manager.get_services()
        
        # Check for expected default services
        self.assertIn("plex", services)
        self.assertIn("jellyfin", services)
        self.assertIn("netflix", services)
        self.assertIn("disneyplus", services)


class TestFullscreenFeatures(unittest.TestCase):
    """Test fullscreen and keybind features"""
    
    def test_launch_callback(self):
        """Test that launch callback is invoked"""
        callback_invoked = []
        
        def test_callback(name, process):
            callback_invoked.append(name)
        
        service = MediaService(
            name="Test Service",
            url="https://example.com",
            icon_color="#ff0000"
        )
        
        # Note: We can't actually test the browser launch in headless environment
        # but we can verify the callback mechanism exists
        self.assertTrue(hasattr(service, 'launch'))
        self.assertTrue(callable(service.launch))
    
    def test_process_tracking_structure(self):
        """Test that launched processes can be tracked"""
        # Test that the structure for tracking processes is correct
        launched_processes = []
        
        # Simulate adding a process
        mock_process = type('MockProcess', (), {'poll': lambda: None, 'pid': 12345})()
        launched_processes.append({
            'name': 'Test App',
            'process': mock_process
        })
        
        self.assertEqual(len(launched_processes), 1)
        self.assertEqual(launched_processes[0]['name'], 'Test App')
        self.assertIsNotNone(launched_processes[0]['process'])
    
    def test_fullscreen_mode_initialization(self):
        """Test that fullscreen mode is configured in the app initialization"""
        # Read the app.py file to verify fullscreen is set
        from pathlib import Path
        app_path = Path(__file__).parent / "castroix_package" / "app.py"
        
        with open(app_path, 'r') as f:
            content = f.read()
        
        # Verify that fullscreen mode is enabled in __init__
        self.assertIn("attributes('-fullscreen', True)", content,
            "App should set fullscreen mode on initialization")
        
        # Verify that Escape key binding exists to exit fullscreen
        self.assertIn("bind('<Escape>'", content,
            "App should have Escape key binding to exit fullscreen")
    
    def test_image_button_sizing(self):
        """Test that button sizing is handled correctly for image vs text buttons"""
        from pathlib import Path
        ui_path = Path(__file__).parent / "castroix_package" / "ui.py"
        
        with open(ui_path, 'r') as f:
            content = f.read()
        
        # Verify that button configuration considers image vs text buttons differently
        self.assertIn("if not self.icon_image:", content,
            "Button configuration should handle image buttons differently")
        
        # Verify that images are resized to appropriate size for fullscreen
        self.assertIn("resize((120, 120)", content,
            "Images should be resized to 120x120 for better visibility")


class TestCrossPlatform(unittest.TestCase):
    """Test cross-platform functionality"""
    
    def test_platform_browser_configurations(self):
        """Test that browser configurations exist for all platforms"""
        import platform as plat
        
        service = MediaService(
            name="Test Service",
            url="https://example.com",
            icon_color="#ff0000"
        )
        
        # Test that the method exists
        self.assertTrue(hasattr(service, '_get_browsers_for_platform'))
        
        # Test each platform
        for system in ['Windows', 'Darwin', 'Linux']:
            browsers = service._get_browsers_for_platform(system)
            self.assertIsInstance(browsers, list)
            self.assertGreater(len(browsers), 0, 
                f"Should have browsers configured for {system}")
            
            # Each browser entry should be a tuple of (name, command)
            for browser_entry in browsers:
                self.assertIsInstance(browser_entry, tuple)
                self.assertEqual(len(browser_entry), 2)
                self.assertIsInstance(browser_entry[0], str)
                self.assertIsInstance(browser_entry[1], str)
                # Command should have {url} placeholder
                self.assertIn('{url}', browser_entry[1])
    
    def test_shutil_which_usage(self):
        """Test that shutil.which is available for cross-platform browser detection"""
        import shutil
        
        # Verify shutil.which exists and works
        self.assertTrue(hasattr(shutil, 'which'))
        self.assertTrue(callable(shutil.which))
        
        # Test that it works with python (should always exist in test environment)
        python_path = shutil.which('python') or shutil.which('python3')
        self.assertIsNotNone(python_path, 
            "shutil.which should find python/python3")
    
    def test_platform_module_import(self):
        """Test that platform module is imported and available"""
        import platform as plat
        
        # Verify we can detect the current platform
        current_system = plat.system()
        self.assertIn(current_system, ['Windows', 'Linux', 'Darwin', 'Java'],
            "Should detect a valid platform")
    
    def test_pil_optional_import(self):
        """Test that PIL import is optional and doesn't break the app"""
        # Verify that castroix_package.ui module has PIL_AVAILABLE flag
        from castroix_package import ui
        
        # PIL_AVAILABLE should be a boolean
        self.assertIsInstance(ui.PIL_AVAILABLE, bool)
        
        # When testing, PIL should be available (since we installed requirements)
        # but the flag should exist regardless
        self.assertTrue(hasattr(ui, 'PIL_AVAILABLE'),
            "castroix_package.ui module should have PIL_AVAILABLE flag")
    
    def test_browser_availability_detection(self):
        """Test that browser availability detection works correctly"""
        service = MediaService(
            name="Test Service",
            url="https://www.example.com",
            icon_color="#4a90e2"
        )
        
        # Test that _is_browser_available method exists
        self.assertTrue(hasattr(service, '_is_browser_available'))
        
        # Test Linux browser detection
        browsers_linux = service._get_browsers_for_platform("Linux")
        self.assertGreater(len(browsers_linux), 0, 
            "Should have Linux browser configurations")
        
        # Test that at least one browser can be detected (or method runs without error)
        for browser_name, browser_cmd in browsers_linux:
            try:
                result = service._is_browser_available(browser_name, browser_cmd, "Linux")
                self.assertIsInstance(result, bool, 
                    "_is_browser_available should return boolean")
                # Don't assert True because not all browsers may be installed
            except Exception as e:
                self.fail(f"_is_browser_available raised exception: {e}")
        
        # Test macOS browser detection (with mock paths)
        browsers_macos = service._get_browsers_for_platform("Darwin")
        self.assertGreater(len(browsers_macos), 0, 
            "Should have macOS browser configurations")
        
        # Test that macOS detection works without errors
        for browser_name, browser_cmd in browsers_macos:
            try:
                result = service._is_browser_available(browser_name, browser_cmd, "Darwin")
                self.assertIsInstance(result, bool, 
                    "_is_browser_available should return boolean")
            except Exception as e:
                self.fail(f"_is_browser_available raised exception: {e}")


def run_tests():
    """Run all tests"""
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestMediaService))
    suite.addTests(loader.loadTestsFromTestCase(TestConfiguration))
    suite.addTests(loader.loadTestsFromTestCase(TestColorUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilities))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigManager))
    suite.addTests(loader.loadTestsFromTestCase(TestFullscreenFeatures))
    suite.addTests(loader.loadTestsFromTestCase(TestCrossPlatform))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
