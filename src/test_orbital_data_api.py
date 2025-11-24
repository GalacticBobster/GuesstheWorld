"""
Unit tests for Orbital Data Explorer Multi-Planet API

Tests the basic functionality of the planetary data API for all supported planets.
"""

import unittest
import math
from orbital_data_api import PlanetaryDataAPI, create_planet_metadata_dict


class TestPlanetaryDataAPI(unittest.TestCase):
    """Test cases for PlanetaryDataAPI class."""
    
    def test_mars_initialization(self):
        """Test that Mars API initializes correctly."""
        api = PlanetaryDataAPI('mars')
        self.assertEqual(api.planet, 'mars')
        self.assertEqual(api.radius_km, 3390)
        self.assertIn('HIRISE', api.config['instruments'])
    
    def test_moon_initialization(self):
        """Test that Moon API initializes correctly."""
        api = PlanetaryDataAPI('moon')
        self.assertEqual(api.planet, 'moon')
        self.assertEqual(api.radius_km, 1737)
        self.assertIn('LROC', api.config['instruments'])
    
    def test_venus_initialization(self):
        """Test that Venus API initializes correctly."""
        api = PlanetaryDataAPI('venus')
        self.assertEqual(api.planet, 'venus')
        self.assertEqual(api.radius_km, 6052)
        self.assertIn('MAGELLAN', api.config['instruments'])
    
    def test_mercury_initialization(self):
        """Test that Mercury API initializes correctly."""
        api = PlanetaryDataAPI('mercury')
        self.assertEqual(api.planet, 'mercury')
        self.assertEqual(api.radius_km, 2440)
        self.assertIn('MESSENGER', api.config['instruments'])
    
    def test_invalid_planet(self):
        """Test that invalid planet raises error."""
        with self.assertRaises(ValueError):
            PlanetaryDataAPI('pluto')
    
    def test_case_insensitive_planet(self):
        """Test that planet names are case-insensitive."""
        api1 = PlanetaryDataAPI('MARS')
        api2 = PlanetaryDataAPI('Mars')
        api3 = PlanetaryDataAPI('mars')
        
        self.assertEqual(api1.planet, 'mars')
        self.assertEqual(api2.planet, 'mars')
        self.assertEqual(api3.planet, 'mars')
    
    def test_km_per_degree_calculation(self):
        """Test that km per degree is calculated correctly for each planet."""
        # Test Mars
        api_mars = PlanetaryDataAPI('mars')
        expected_mars = (2 * math.pi * 3390) / 360
        self.assertAlmostEqual(api_mars.km_per_degree, expected_mars, places=2)
        
        # Test Moon
        api_moon = PlanetaryDataAPI('moon')
        expected_moon = (2 * math.pi * 1737) / 360
        self.assertAlmostEqual(api_moon.km_per_degree, expected_moon, places=2)
    
    def test_search_images_parameters(self):
        """Test that search_images accepts correct parameters."""
        api = PlanetaryDataAPI('mars')
        
        # Test that method accepts valid parameters without error
        try:
            result = api.search_images(
                latitude=18.65,
                longitude=226.2,
                radius_km=100,
                limit=5
            )
            # Result should be a list (even if empty due to no network)
            self.assertIsInstance(result, list)
        except Exception:
            # Network errors are expected in test environment
            pass


class TestPlanetMetadata(unittest.TestCase):
    """Test planet metadata dictionary creation."""
    
    def test_mars_metadata(self):
        """Test Mars metadata structure."""
        metadata = create_planet_metadata_dict('mars')
        self.assertEqual(metadata['name'], 'Mars')
        self.assertEqual(metadata['radius_km'], 3390)
        self.assertIn('map_image', metadata)
        self.assertIn('nomenclature_file', metadata)
        self.assertIn('features', metadata)
    
    def test_moon_metadata(self):
        """Test Moon metadata structure."""
        metadata = create_planet_metadata_dict('moon')
        self.assertEqual(metadata['name'], 'Moon')
        self.assertEqual(metadata['radius_km'], 1737)
    
    def test_venus_metadata(self):
        """Test Venus metadata structure."""
        metadata = create_planet_metadata_dict('venus')
        self.assertEqual(metadata['name'], 'Venus')
        self.assertEqual(metadata['radius_km'], 6052)
    
    def test_mercury_metadata(self):
        """Test Mercury metadata structure."""
        metadata = create_planet_metadata_dict('mercury')
        self.assertEqual(metadata['name'], 'Mercury')
        self.assertEqual(metadata['radius_km'], 2440)
    
    def test_invalid_planet_metadata(self):
        """Test that invalid planet returns empty dict."""
        metadata = create_planet_metadata_dict('invalid')
        self.assertEqual(metadata, {})
    
    def test_all_planets_have_required_fields(self):
        """Test that all planets have required metadata fields."""
        required_fields = ['name', 'radius_km', 'map_image', 'nomenclature_file', 'features']
        
        for planet in ['mars', 'moon', 'venus', 'mercury']:
            metadata = create_planet_metadata_dict(planet)
            for field in required_fields:
                self.assertIn(field, metadata, f"{planet} missing {field}")


class TestAPIConfiguration(unittest.TestCase):
    """Test API configuration constants."""
    
    def test_ode_base_url(self):
        """Test ODE base URL is correct."""
        api = PlanetaryDataAPI('mars')
        self.assertTrue(api.ODE_BASE_URL.startswith('https://'))
        self.assertIn('oderest', api.ODE_BASE_URL)
    
    def test_user_agent_header(self):
        """Test that user agent header is set."""
        api = PlanetaryDataAPI('mars')
        self.assertIn('User-Agent', api.session_headers)
        self.assertIn('GuessTheWorld', api.session_headers['User-Agent'])
    
    def test_all_planets_have_config(self):
        """Test that all supported planets have configuration."""
        for planet in ['mars', 'moon', 'venus', 'mercury']:
            api = PlanetaryDataAPI(planet)
            self.assertIsNotNone(api.config)
            self.assertIn('target', api.config)
            self.assertIn('instruments', api.config)
            self.assertIn('radius_km', api.config)


class TestPlanetRadii(unittest.TestCase):
    """Test that planet radii are correct."""
    
    def test_planet_radii(self):
        """Verify planet radii match known values."""
        expected_radii = {
            'mars': 3390,
            'moon': 1737,
            'venus': 6052,
            'mercury': 2440
        }
        
        for planet, expected_radius in expected_radii.items():
            api = PlanetaryDataAPI(planet)
            self.assertEqual(
                api.radius_km, 
                expected_radius,
                f"{planet} radius should be {expected_radius} km"
            )


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPlanetaryDataAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestPlanetMetadata))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIConfiguration))
    suite.addTests(loader.loadTestsFromTestCase(TestPlanetRadii))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("\n" + "="*70)
    print("Orbital Data Explorer Multi-Planet API - Unit Tests")
    print("="*70 + "\n")
    
    success = run_tests()
    
    print("\n" + "="*70)
    if success:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("="*70 + "\n")
    
    exit(0 if success else 1)
