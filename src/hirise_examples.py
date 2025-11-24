"""
Example Usage of Mars HIRISE Multi-Scale Imaging API

This script demonstrates how to use the HIRISE API for accessing Mars images
at different scales and resolutions.
"""

from mars_hirise_api import HiriseAPI
from PIL import Image


def example_1_basic_search():
    """Example 1: Basic image search by location."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Search for HIRISE images by location")
    print("="*60)
    
    api = HiriseAPI()
    
    # Search for images near Valles Marineris
    # Latitude: -13.9, Longitude: 301.3 (West)
    print("\nSearching for images near Valles Marineris...")
    results = api.search_images(
        latitude=-13.9,
        longitude=301.3,
        radius_km=200,
        limit=10
    )
    
    print(f"\nFound {len(results)} images:")
    for i, result in enumerate(results, 1):
        product_id = result.get('pdsid') or result.get('ProductId') or 'Unknown'
        center_lat = result.get('Center_Latitude') or result.get('CenterLatitude') or 'N/A'
        center_lon = result.get('Center_Longitude') or result.get('CenterLongitude') or 'N/A'
        print(f"  {i}. {product_id}")
        print(f"     Location: ({center_lat}, {center_lon})")


def example_2_multi_scale_tiles():
    """Example 2: Get multi-scale tile URLs for an image."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Multi-scale tile pyramid access")
    print("="*60)
    
    api = HiriseAPI()
    
    # Example HIRISE product ID
    # In real usage, you would get this from a search result
    product_id = "ESP_016644_1755"
    
    print(f"\nGetting multi-scale tiles for {product_id}...")
    print("Scale levels: 1 (full res), 2 (half), 4 (quarter), 8 (eighth)")
    
    tile_urls = api.get_multi_scale_tiles(
        product_id,
        scale_levels=[1, 2, 4, 8, 16]
    )
    
    print("\nTile URLs:")
    for scale, url in sorted(tile_urls.items()):
        print(f"  Scale {scale:2d}x: {url}")


def example_3_download_image():
    """Example 3: Download and process an image at specific scale."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Download image at specific scale")
    print("="*60)
    
    api = HiriseAPI()
    
    # Example: Download a browse image
    product_id = "ESP_016644_1755"
    
    print(f"\nAttempting to download image for {product_id} at scale 8x...")
    print("(This would download an actual image if the product exists)")
    
    # Get the image at reduced scale (8x downsampled = 1/8 resolution)
    # This is useful for previews and quick loading
    image = api.get_image_at_scale(product_id, scale=8)
    
    if image:
        print(f"Successfully loaded image: {image.size[0]}x{image.size[1]} pixels")
        # You can now process or display the image
        # image.show()  # Uncomment to display
        # image.save("hirise_preview.jpg")  # Uncomment to save
    else:
        print("Image download failed (product may not exist or be unavailable)")


def example_4_metadata_retrieval():
    """Example 4: Retrieve detailed metadata for an image."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Retrieve image metadata")
    print("="*60)
    
    api = HiriseAPI()
    
    product_id = "ESP_016644_1755"
    
    print(f"\nFetching metadata for {product_id}...")
    metadata = api.get_image_metadata(product_id)
    
    if metadata:
        print("\nImage Metadata:")
        print(f"  Product ID: {metadata.get('pdsid') or metadata.get('ProductId')}")
        print(f"  Center Latitude: {metadata.get('Center_Latitude') or metadata.get('CenterLatitude')}")
        print(f"  Center Longitude: {metadata.get('Center_Longitude') or metadata.get('CenterLongitude')}")
        print(f"  Target: {metadata.get('Target')}")
        
        # Additional fields may be available depending on the API response
        if 'Description' in metadata:
            print(f"  Description: {metadata['Description']}")
    else:
        print("Could not retrieve metadata (product may not exist)")


def example_5_location_based_workflow():
    """Example 5: Complete workflow - search, select, and load at multiple scales."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Complete multi-scale imaging workflow")
    print("="*60)
    
    api = HiriseAPI()
    
    # Step 1: Search for images
    print("\nStep 1: Searching for images near Gale Crater...")
    results = api.search_images(
        latitude=-5.4,
        longitude=137.8,
        radius_km=50,
        limit=5
    )
    
    if results:
        print(f"Found {len(results)} images")
        
        # Step 2: Select first result
        first_result = results[0]
        product_id = first_result.get('pdsid') or first_result.get('ProductId')
        print(f"\nStep 2: Selected {product_id}")
        
        # Step 3: Get location info
        location = api.get_location_info(product_id)
        if location:
            print(f"Step 3: Image location: {location[0]:.2f}°, {location[1]:.2f}°")
        
        # Step 4: Get multi-scale tile URLs
        print("\nStep 4: Getting multi-scale tiles...")
        tiles = api.get_multi_scale_tiles(product_id, [1, 2, 4, 8])
        for scale in sorted(tiles.keys()):
            print(f"  Scale {scale}x available")
        
        # Step 5: In a real application, you would:
        # - Load the lowest resolution (8x) for quick preview
        # - Load medium resolution (4x) for browsing
        # - Load high resolution (1x) for detailed examination
        print("\nStep 5: Images ready for multi-scale viewing")
        print("  Use case: Progressive image loading for better UX")
    else:
        print("No images found in search area")


def example_6_custom_scaling():
    """Example 6: Download and apply custom scaling."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Custom image scaling")
    print("="*60)
    
    api = HiriseAPI()
    
    product_id = "ESP_016644_1755"
    
    print(f"\nDemonstrating custom scaling for {product_id}...")
    
    # Get tile URL
    tiles = api.get_multi_scale_tiles(product_id, [8])
    if 8 in tiles:
        url = tiles[8]
        
        # Download with custom scale factors
        scales = [0.5, 1.0, 2.0]
        print("\nDownloading with different scale factors:")
        for scale in scales:
            print(f"  Scale factor {scale}x:")
            image = api.download_image(url, scale=scale)
            if image:
                print(f"    Result: {image.size[0]}x{image.size[1]} pixels")
            else:
                print(f"    Download failed")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("Mars HIRISE Multi-Scale Imaging API - Usage Examples")
    print("="*60)
    print("\nThese examples demonstrate various features of the HIRISE API:")
    print("- Searching for images by geographic location")
    print("- Accessing images at different scale levels")
    print("- Retrieving metadata and location information")
    print("- Implementing multi-scale viewing workflows")
    print("\nNote: Some examples may not return actual data if the API is")
    print("      offline or the example product IDs don't exist.")
    
    # Run each example
    example_1_basic_search()
    example_2_multi_scale_tiles()
    example_3_download_image()
    example_4_metadata_retrieval()
    example_5_location_based_workflow()
    example_6_custom_scaling()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()
