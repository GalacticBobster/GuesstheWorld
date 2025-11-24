"""
Orbital Data Explorer (ODE) API for Multi-Planet Imaging

This module provides a unified API for accessing planetary images from NASA's
Orbital Data Explorer (ODE) system. Supports multiple planets and their missions:
- Mars: HIRISE (High Resolution Imaging Science Experiment)
- Moon: LRO (Lunar Reconnaissance Orbiter)
- Venus: Magellan Radar Mission
- Mercury: MESSENGER mission

Key Features:
- Fetch planetary images at different resolutions
- Access image metadata
- Support for multi-planet data access
- Integration with ODE REST API

References:
- ODE REST API: https://oderest.rsl.wustl.edu/
"""

import urllib.request
import urllib.parse
import json
from typing import Dict, List, Optional, Tuple
from PIL import Image
import io


class PlanetaryDataAPI:
    """API client for planetary data from ODE."""
    
    # ODE REST API base URL
    ODE_BASE_URL = "https://oderest.rsl.wustl.edu/live2"
    
    # Planet-specific configurations
    PLANET_CONFIG = {
        'mars': {
            'target': 'mars',
            'instruments': ['HIRISE', 'CTX', 'MOC'],
            'radius_km': 3390,  # Mars mean radius
            'image_base': 'https://hirise.lpl.arizona.edu'
        },
        'moon': {
            'target': 'moon',
            'instruments': ['LROC', 'NAC', 'WAC'],
            'radius_km': 1737,  # Moon mean radius
            'image_base': 'https://wms.lroc.asu.edu'
        },
        'venus': {
            'target': 'venus',
            'instruments': ['MAGELLAN'],
            'radius_km': 6052,  # Venus mean radius
            'image_base': None  # Venus data through ODE
        },
        'mercury': {
            'target': 'mercury',
            'instruments': ['MESSENGER', 'MDIS'],
            'radius_km': 2440,  # Mercury mean radius
            'image_base': None  # Mercury data through ODE
        }
    }
    
    def __init__(self, planet: str = 'mars'):
        """
        Initialize the planetary data API client.
        
        Args:
            planet: Target planet ('mars', 'moon', 'venus', or 'mercury')
        """
        self.planet = planet.lower()
        if self.planet not in self.PLANET_CONFIG:
            raise ValueError(f"Unsupported planet: {planet}. Choose from: {list(self.PLANET_CONFIG.keys())}")
        
        self.config = self.PLANET_CONFIG[self.planet]
        self.radius_km = self.config['radius_km']
        self.km_per_degree = (2 * 3.14159 * self.radius_km) / 360
        
        self.session_headers = {
            'User-Agent': 'GuessTheWorld-PlanetaryAPI/1.0'
        }
    
    def search_images(self, 
                     latitude: Optional[float] = None,
                     longitude: Optional[float] = None,
                     radius_km: Optional[float] = None,
                     limit: int = 10) -> List[Dict]:
        """
        Search for images by location.
        
        Args:
            latitude: Center latitude for search (-90 to 90)
            longitude: Center longitude for search (0 to 360)
            radius_km: Search radius in kilometers
            limit: Maximum number of results to return
            
        Returns:
            List of image metadata dictionaries
        """
        params = {
            'query': self.config['target'],
            'results': 'c',
            'output': 'JSON',
            'limit': limit
        }
        
        if latitude is not None and longitude is not None:
            # Convert radius from km to degrees
            degree_radius = (radius_km / self.km_per_degree) if radius_km else 5
            params['minlat'] = max(latitude - degree_radius, -90)
            params['maxlat'] = min(latitude + degree_radius, 90)
            params['westlon'] = longitude - degree_radius
            params['eastlon'] = longitude + degree_radius
        
        # Build query URL
        query_url = f"{self.ODE_BASE_URL}?{urllib.parse.urlencode(params)}"
        
        try:
            request = urllib.request.Request(query_url, headers=self.session_headers)
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
                
            # Parse and return results
            if 'ODEResults' in data and 'Products' in data['ODEResults']:
                products = data['ODEResults']['Products'].get('Product', [])
                if isinstance(products, dict):
                    products = [products]
                return products[:limit]
            return []
            
        except Exception as e:
            print(f"Error searching {self.planet} images: {e}")
            return []
    
    def get_image_metadata(self, product_id: str) -> Optional[Dict]:
        """
        Get detailed metadata for a specific image.
        
        Args:
            product_id: Product ID (e.g., "ESP_012345_1234" for Mars)
            
        Returns:
            Dictionary containing image metadata
        """
        params = {
            'query': product_id,
            'results': 'c',
            'output': 'JSON'
        }
        
        query_url = f"{self.ODE_BASE_URL}?{urllib.parse.urlencode(params)}"
        
        try:
            request = urllib.request.Request(query_url, headers=self.session_headers)
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
                
            if 'ODEResults' in data and 'Products' in data['ODEResults']:
                products = data['ODEResults']['Products'].get('Product', [])
                if isinstance(products, list) and len(products) > 0:
                    return products[0]
                elif isinstance(products, dict):
                    return products
            return None
            
        except Exception as e:
            print(f"Error fetching metadata for {product_id}: {e}")
            return None
    
    def get_location_info(self, product_id: str) -> Optional[Tuple[float, float]]:
        """
        Get the center latitude and longitude for an image.
        
        Args:
            product_id: Product ID
            
        Returns:
            Tuple of (latitude, longitude) or None if not available
        """
        metadata = self.get_image_metadata(product_id)
        if metadata:
            # Extract location from metadata
            lat = metadata.get('Center_Latitude') or metadata.get('CenterLatitude')
            lon = metadata.get('Center_Longitude') or metadata.get('CenterLongitude')
            
            if lat is not None and lon is not None:
                try:
                    return (float(lat), float(lon))
                except (ValueError, TypeError):
                    pass
        return None
    
    def download_image(self, url: str, scale: float = 1.0) -> Optional[Image.Image]:
        """
        Download and load an image from a URL.
        
        Args:
            url: URL of the image to download
            scale: Scale factor to resize the image (1.0 = original size)
            
        Returns:
            PIL Image object or None if download fails
        """
        try:
            request = urllib.request.Request(url, headers=self.session_headers)
            with urllib.request.urlopen(request, timeout=60) as response:
                image_data = response.read()
            
            image = Image.open(io.BytesIO(image_data))
            
            # Apply scaling if requested
            if scale != 1.0:
                new_size = (int(image.width * scale), int(image.height * scale))
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            return image
            
        except Exception as e:
            print(f"Error downloading image from {url}: {e}")
            return None


def create_planet_metadata_dict(planet: str) -> Dict:
    """
    Create a metadata dictionary for a planet with nomenclature/feature data.
    
    Args:
        planet: Planet name ('mars', 'moon', 'venus', 'mercury')
    
    Returns:
        Dictionary with planet metadata including features for guessing game
    """
    # These would be populated from KMZ/KML files or ODE queries
    # For now, returning structure with example data
    
    planet_metadata = {
        'mars': {
            'name': 'Mars',
            'radius_km': 3390,
            'map_image': 'mars_viking_clrmosaic_global_1024.jpg',
            'nomenclature_file': 'MARS_nomenclature_center_pts.kmz',
            'features': []  # Would be loaded from KMZ
        },
        'moon': {
            'name': 'Moon',
            'radius_km': 1737,
            'map_image': 'moon_lro_clrshade_global_1024.jpg',
            'nomenclature_file': 'MOON_nomenclature_center_pts.kmz',
            'features': []  # Would be loaded from KMZ
        },
        'venus': {
            'name': 'Venus',
            'radius_km': 6052,
            'map_image': 'venus_magellan_global_1024.jpg',
            'nomenclature_file': 'VENUS_nomenclature_center_pts.kmz',
            'features': []  # Would be loaded from KMZ
        },
        'mercury': {
            'name': 'Mercury',
            'radius_km': 2440,
            'map_image': 'mercury_messenger_global_1024.jpg',
            'nomenclature_file': 'MERCURY_nomenclature_center_pts.kmz',
            'features': []  # Would be loaded from KMZ
        }
    }
    
    return planet_metadata.get(planet.lower(), {})


if __name__ == "__main__":
    print("Orbital Data Explorer Multi-Planet API")
    print("=" * 50)
    
    # Demonstrate API for each planet
    for planet in ['mars', 'moon', 'venus', 'mercury']:
        print(f"\n{planet.upper()} API:")
        try:
            api = PlanetaryDataAPI(planet)
            print(f"  Radius: {api.radius_km} km")
            print(f"  Instruments: {api.config['instruments']}")
            print(f"  API initialized successfully")
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n" + "=" * 50)
    print("API Demo Complete!")
