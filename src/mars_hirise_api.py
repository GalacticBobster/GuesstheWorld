"""
Mars HIRISE API for Multi-Scale Imaging

This module provides an API for accessing Mars High Resolution Imaging Science Experiment (HIRISE) 
images at multiple scales. HIRISE is a camera aboard the Mars Reconnaissance Orbiter that provides
high-resolution images of the Martian surface.

Key Features:
- Fetch HIRISE images at different resolutions/scales
- Access image metadata
- Support for multi-scale tile-based viewing
- Integration with ODE (Orbital Data Explorer) REST API

References:
- HIRISE website: https://hirise.lpl.arizona.edu/
- ODE REST API: https://oderest.rsl.wustl.edu/
"""

import urllib.request
import urllib.parse
import json
from typing import Dict, List, Optional, Tuple
from PIL import Image
import io


class HiriseAPI:
    """API client for Mars HIRISE multi-scale imaging."""
    
    # HIRISE ODE REST API base URL
    ODE_BASE_URL = "https://oderest.rsl.wustl.edu/live2"
    
    # HIRISE public image server
    HIRISE_IMAGE_BASE = "https://hirise.lpl.arizona.edu"
    
    def __init__(self):
        """Initialize the HIRISE API client."""
        self.session_headers = {
            'User-Agent': 'GuessTheWorld-HIRISE-API/1.0'
        }
    
    def search_images(self, 
                     latitude: Optional[float] = None,
                     longitude: Optional[float] = None,
                     radius_km: Optional[float] = None,
                     limit: int = 10) -> List[Dict]:
        """
        Search for HIRISE images by location.
        
        Args:
            latitude: Center latitude for search (-90 to 90)
            longitude: Center longitude for search (0 to 360)
            radius_km: Search radius in kilometers
            limit: Maximum number of results to return
            
        Returns:
            List of image metadata dictionaries
        """
        params = {
            'query': 'mars',
            'results': 'c',
            'output': 'JSON',
            'limit': limit
        }
        
        if latitude is not None and longitude is not None:
            # Add spatial query parameters
            params['minlat'] = latitude - (radius_km / 111.0 if radius_km else 5)
            params['maxlat'] = latitude + (radius_km / 111.0 if radius_km else 5)
            params['westlon'] = longitude - (radius_km / 111.0 if radius_km else 5)
            params['eastlon'] = longitude + (radius_km / 111.0 if radius_km else 5)
        
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
            print(f"Error searching HIRISE images: {e}")
            return []
    
    def get_image_metadata(self, product_id: str) -> Optional[Dict]:
        """
        Get detailed metadata for a specific HIRISE image.
        
        Args:
            product_id: HIRISE product ID (e.g., "ESP_012345_1234")
            
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
    
    def get_multi_scale_tiles(self, product_id: str, scale_levels: List[int] = None) -> Dict[int, str]:
        """
        Get URLs for multi-scale tile pyramids of a HIRISE image.
        
        HIRISE images are often provided in multi-resolution pyramids for efficient viewing
        at different zoom levels.
        
        Args:
            product_id: HIRISE product ID
            scale_levels: List of scale levels to fetch (e.g., [1, 2, 4, 8] for different zoom levels)
                         Level 1 is full resolution, higher numbers are downsampled
            
        Returns:
            Dictionary mapping scale level to tile URL pattern
        """
        if scale_levels is None:
            scale_levels = [1, 2, 4, 8]
        
        # HIRISE tile URL pattern (example structure)
        # Actual implementation would depend on HIRISE tile server configuration
        tile_urls = {}
        
        for scale in scale_levels:
            # Standard HIRISE browse product structure
            # RED (visible wavelength) browse images are commonly available
            tile_pattern = f"{self.HIRISE_IMAGE_BASE}/PDS/RDR/{product_id}/{product_id}_RED.browse.jpg"
            if scale > 1:
                # For downsampled versions, some servers provide _browse2, _browse4, etc.
                tile_pattern = f"{self.HIRISE_IMAGE_BASE}/PDS/RDR/{product_id}/{product_id}_RED.browse{scale}.jpg"
            tile_urls[scale] = tile_pattern
        
        return tile_urls
    
    def download_image(self, url: str, scale: float = 1.0) -> Optional[Image.Image]:
        """
        Download and load a HIRISE image from a URL.
        
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
    
    def get_image_at_scale(self, product_id: str, scale: int = 1) -> Optional[Image.Image]:
        """
        Get a HIRISE image at a specific scale level.
        
        Args:
            product_id: HIRISE product ID
            scale: Scale level (1=full resolution, 2=half, 4=quarter, etc.)
            
        Returns:
            PIL Image object or None if download fails
        """
        tile_urls = self.get_multi_scale_tiles(product_id, [scale])
        if scale in tile_urls:
            return self.download_image(tile_urls[scale])
        return None
    
    def get_location_info(self, product_id: str) -> Optional[Tuple[float, float]]:
        """
        Get the center latitude and longitude for a HIRISE image.
        
        Args:
            product_id: HIRISE product ID
            
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


# Example usage functions
def demo_search():
    """Demonstrate searching for HIRISE images."""
    api = HiriseAPI()
    
    # Search for images near Olympus Mons
    print("Searching for HIRISE images near Olympus Mons...")
    results = api.search_images(latitude=18.65, longitude=226.2, radius_km=100, limit=5)
    
    print(f"Found {len(results)} images")
    for i, result in enumerate(results, 1):
        product_id = result.get('pdsid') or result.get('ProductId') or 'Unknown'
        print(f"{i}. {product_id}")
    
    return results


def demo_multi_scale():
    """Demonstrate multi-scale image access."""
    api = HiriseAPI()
    
    # Example product ID (this would be a real HIRISE ID in practice)
    product_id = "ESP_012345_1234"
    
    print(f"\nGetting multi-scale tiles for {product_id}...")
    tiles = api.get_multi_scale_tiles(product_id)
    
    for scale, url in sorted(tiles.items()):
        print(f"Scale {scale}x: {url}")
    
    return tiles


if __name__ == "__main__":
    print("Mars HIRISE Multi-Scale Imaging API Demo")
    print("=" * 50)
    
    # Run demonstrations
    demo_search()
    demo_multi_scale()
    
    print("\n" + "=" * 50)
    print("API Demo Complete!")
