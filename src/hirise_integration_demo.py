"""
Integration Example: Using HIRISE API with Mars Guessing Game

This example demonstrates how the new HIRISE API can be integrated with
the existing Mars_thinker.py game to enhance it with high-resolution
HIRISE images.
"""

from mars_hirise_api import HiriseAPI
from PIL import Image


def example_integration():
    """
    Example: Enhance the Mars guessing game with HIRISE images.
    
    This shows how you could modify Mars_thinker.py to use HIRISE images
    alongside the existing Viking mosaic.
    """
    print("="*70)
    print("HIRISE API Integration Example")
    print("="*70)
    
    # Initialize HIRISE API
    api = HiriseAPI()
    
    # Example: Get a HIRISE image for a specific Mars feature
    # Let's use Olympus Mons as an example
    feature_name = "Olympus Mons"
    latitude = 18.65
    longitude = 226.2
    
    print(f"\n1. Searching for HIRISE images near {feature_name}...")
    print(f"   Location: ({latitude}°, {longitude}°)")
    
    results = api.search_images(
        latitude=latitude,
        longitude=longitude,
        radius_km=100,
        limit=5
    )
    
    if results:
        print(f"   Found {len(results)} HIRISE images!")
        
        # Get the first result
        product_id = results[0].get('pdsid') or results[0].get('ProductId')
        print(f"\n2. Selected image: {product_id}")
        
        # Get multi-scale tiles
        print("\n3. Getting multi-scale image pyramid...")
        tiles = api.get_multi_scale_tiles(product_id, [1, 2, 4, 8])
        
        for scale, url in sorted(tiles.items()):
            print(f"   Scale {scale}x: Available")
        
        # Demonstrate how this would be used in the game
        print("\n4. Integration approach:")
        print("   - Load scale 8x for initial preview (fast)")
        print("   - Load scale 4x when user guesses correctly (medium detail)")
        print("   - Load scale 1x for final reveal (full resolution)")
        print("\n5. Benefit: Progressive loading improves user experience!")
        
    else:
        print("   No images found (this is expected if network is unavailable)")
    
    print("\n" + "="*70)
    print("Integration Example Complete!")
    print("="*70)


def example_enhanced_game_logic():
    """
    Example: Enhanced game logic with HIRISE support.
    
    This shows pseudo-code for how to enhance the existing game.
    """
    print("\n" + "="*70)
    print("Enhanced Game Logic Example")
    print("="*70)
    
    print("""
    # In Mars_thinker.py, you could add:
    
    class MarsGuessGame:
        def __init__(self, master, mars_img, points):
            # ... existing code ...
            self.hirise_api = HiriseAPI()  # Add HIRISE API
            
        def next_round(self):
            # ... existing code to get target location ...
            
            # Try to get HIRISE image for this location
            hirise_results = self.hirise_api.search_images(
                latitude=lat,
                longitude=lon,
                radius_km=50,
                limit=1
            )
            
            if hirise_results:
                # Use HIRISE high-res image
                product_id = hirise_results[0].get('pdsid')
                patch = self.hirise_api.get_image_at_scale(
                    product_id, 
                    scale=8  # Start with preview
                )
            else:
                # Fallback to existing Viking mosaic
                patch = self.mars_img.crop((left, upper, right, lower))
            
            # ... rest of existing code ...
        
        def check_guess(self):
            # ... existing code ...
            
            if guess_correct and self.hirise_image_available:
                # Reveal higher resolution on correct guess
                detail_image = self.hirise_api.get_image_at_scale(
                    self.current_product_id,
                    scale=2  # Higher detail
                )
                # Show the detailed image
    """)
    
    print("="*70)
    print("This demonstrates how HIRISE API enhances the game without")
    print("breaking existing functionality.")
    print("="*70)


def example_features_summary():
    """Display a summary of what the HIRISE API provides."""
    print("\n" + "="*70)
    print("HIRISE API Features Summary")
    print("="*70)
    
    features = [
        ("Multi-Scale Access", "Load images at 1x, 2x, 4x, 8x for progressive viewing"),
        ("Location Search", "Find HIRISE images anywhere on Mars by lat/lon"),
        ("Metadata", "Get image details, dates, and coordinates"),
        ("High Resolution", "Access the highest resolution Mars images available"),
        ("Progressive Loading", "Fast preview → medium detail → full resolution"),
        ("Easy Integration", "Simple API that works with existing PIL/Pillow code"),
    ]
    
    print("\nKey Features:")
    for i, (feature, description) in enumerate(features, 1):
        print(f"\n{i}. {feature}")
        print(f"   {description}")
    
    print("\n" + "="*70)
    print("The API is production-ready and can enhance Mars visualization!")
    print("="*70)


if __name__ == "__main__":
    print("\n" + "="*70)
    print("Mars HIRISE API - Integration Demonstration")
    print("="*70)
    print("\nThis demonstrates how the new HIRISE API integrates with")
    print("the existing Mars guessing game without modifying existing files.")
    
    # Run examples
    example_integration()
    example_enhanced_game_logic()
    example_features_summary()
    
    print("\n" + "="*70)
    print("All Integration Examples Complete!")
    print("="*70 + "\n")
