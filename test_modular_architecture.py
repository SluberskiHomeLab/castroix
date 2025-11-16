#!/usr/bin/env python3
"""
Unit tests for the new modular architecture.
Tests the separation of concerns and modularity.
"""
import unittest
import json
import tempfile
from pathlib import Path

# Import the modular components
from castroix.config import ConfigManager
from castroix.services import MediaService, ServiceManager


class TestConfigManager(unittest.TestCase):
    """Test ConfigManager class"""
    
    def setUp(self):
        """Setup test configuration"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_config = Path(self.temp_dir) / "test_config.json"
    
    def tearDown(self):
        """Cleanup test files"""
        if self.temp_config.exists():
            self.temp_config.unlink()
        Path(self.temp_dir).rmdir()
    
    def test_config_manager_init(self):
        """Test ConfigManager initialization"""
        config_manager = ConfigManager(self.temp_config)
        self.assertEqual(config_manager.config_path, self.temp_config)
    
    def test_config_manager_load_default(self):
        """Test loading default configuration"""
        config_manager = ConfigManager(self.temp_config)
        config = config_manager.load()
        
        # Should have default services
        self.assertIn("services", config)
        self.assertIn("plex", config["services"])
        self.assertIn("jellyfin", config["services"])
        self.assertIn("netflix", config["services"])
        self.assertIn("disneyplus", config["services"])
    
    def test_config_manager_save_and_load(self):
        """Test saving and loading configuration"""
        config_manager = ConfigManager(self.temp_config)
        
        # Create custom config
        custom_config = {
            "services": {
                "test_service": {
                    "name": "Test Service",
                    "url": "https://test.com",
                    "command": None,
                    "icon_color": "#ff0000",
                    "icon_file": "test.png"
                }
            }
        }
        
        # Save config
        config_manager.save(custom_config)
        
        # Load config
        loaded_config = config_manager.load()
        
        # Verify it matches
        self.assertEqual(loaded_config, custom_config)
        self.assertIn("test_service", loaded_config["services"])
    
    def test_config_manager_get_services(self):
        """Test getting services from configuration"""
        config_manager = ConfigManager(self.temp_config)
        config_manager.load()
        
        services = config_manager.get_services()
        
        # Should return services dictionary
        self.assertIsInstance(services, dict)
        self.assertGreater(len(services), 0)


class TestServiceManager(unittest.TestCase):
    """Test ServiceManager class"""
    
    def test_service_manager_init(self):
        """Test ServiceManager initialization"""
        services_config = {
            "test1": {
                "name": "Test 1",
                "url": "https://test1.com",
                "icon_color": "#ff0000"
            },
            "test2": {
                "name": "Test 2",
                "url": "https://test2.com",
                "icon_color": "#00ff00"
            }
        }
        
        service_manager = ServiceManager(services_config)
        self.assertIsNotNone(service_manager.services)
        self.assertEqual(len(service_manager.services), 2)
    
    def test_service_manager_get_services(self):
        """Test getting services from ServiceManager"""
        services_config = {
            "plex": {
                "name": "Plex",
                "url": "https://app.plex.tv",
                "icon_color": "#e5a00d",
                "icon_file": "plex.png"
            }
        }
        
        service_manager = ServiceManager(services_config)
        services = service_manager.get_services()
        
        # Should return list of MediaService objects
        self.assertIsInstance(services, list)
        self.assertEqual(len(services), 1)
        self.assertIsInstance(services[0], MediaService)
        self.assertEqual(services[0].name, "Plex")
        self.assertEqual(services[0].url, "https://app.plex.tv")
        self.assertEqual(services[0].icon_color, "#e5a00d")


class TestModularSeparation(unittest.TestCase):
    """Test separation of concerns in modular architecture"""
    
    def test_config_module_exists(self):
        """Test that config module exists and is separate"""
        from castroix import config
        self.assertTrue(hasattr(config, 'ConfigManager'))
    
    def test_services_module_exists(self):
        """Test that services module exists and is separate"""
        from castroix import services
        self.assertTrue(hasattr(services, 'MediaService'))
        self.assertTrue(hasattr(services, 'ServiceManager'))
    
    def test_package_exports(self):
        """Test that package exports the right components"""
        import castroix
        
        # Check main exports
        self.assertTrue(hasattr(castroix, 'ConfigManager'))
        self.assertTrue(hasattr(castroix, 'MediaService'))
        self.assertTrue(hasattr(castroix, 'ServiceManager'))
        self.assertTrue(hasattr(castroix, 'CastroixUI'))
        self.assertTrue(hasattr(castroix, 'PIL_AVAILABLE'))
        self.assertTrue(hasattr(castroix, '__version__'))
    
    def test_version_exists(self):
        """Test that version is defined"""
        import castroix
        self.assertIsInstance(castroix.__version__, str)
        self.assertRegex(castroix.__version__, r'\d+\.\d+\.\d+')


class TestBackwardCompatibility(unittest.TestCase):
    """Test backward compatibility with original structure"""
    
    def test_original_castroix_imports(self):
        """Test that original imports still work"""
        # This should work for backward compatibility
        from castroix import MediaService, ConfigManager, ServiceManager
        
        # Create instances to verify they work
        service = MediaService("Test", url="https://test.com")
        self.assertEqual(service.name, "Test")
    
    def test_media_service_interface(self):
        """Test that MediaService has the expected interface"""
        service = MediaService(
            name="Test",
            url="https://test.com",
            command=None,
            icon_color="#ff0000",
            icon_file="test.png"
        )
        
        # Check attributes
        self.assertEqual(service.name, "Test")
        self.assertEqual(service.url, "https://test.com")
        self.assertIsNone(service.command)
        self.assertEqual(service.icon_color, "#ff0000")
        self.assertEqual(service.icon_file, "test.png")
        
        # Check methods
        self.assertTrue(hasattr(service, 'launch'))
        self.assertTrue(callable(service.launch))


class TestIntegration(unittest.TestCase):
    """Integration tests for the modular architecture"""
    
    def test_full_flow(self):
        """Test complete flow from config to services"""
        # Create temporary config
        temp_dir = tempfile.mkdtemp()
        temp_config = Path(temp_dir) / "test_config.json"
        
        try:
            # Create config manager
            config_manager = ConfigManager(temp_config)
            
            # Load default config
            config = config_manager.load()
            services_config = config_manager.get_services()
            
            # Create service manager
            service_manager = ServiceManager(services_config)
            services = service_manager.get_services()
            
            # Verify we have services
            self.assertIsInstance(services, list)
            self.assertGreater(len(services), 0)
            
            # Verify services are MediaService objects
            for service in services:
                self.assertIsInstance(service, MediaService)
                self.assertIsNotNone(service.name)
                self.assertIsNotNone(service.icon_color)
        
        finally:
            # Cleanup
            if temp_config.exists():
                temp_config.unlink()
            Path(temp_dir).rmdir()


def run_tests():
    """Run all tests"""
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestConfigManager))
    suite.addTests(loader.loadTestsFromTestCase(TestServiceManager))
    suite.addTests(loader.loadTestsFromTestCase(TestModularSeparation))
    suite.addTests(loader.loadTestsFromTestCase(TestBackwardCompatibility))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
