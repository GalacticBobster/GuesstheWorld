# Mars HIRISE Multi-Scale Imaging API

This module provides a Python API for accessing Mars High Resolution Imaging Science Experiment (HIRISE) images at multiple scales.

## Overview

HIRISE is a camera aboard NASA's Mars Reconnaissance Orbiter that provides the highest resolution images of the Martian surface. This API enables:

- **Multi-scale image access**: Retrieve images at different resolution levels for efficient viewing
- **Location-based search**: Find HIRISE images by geographic coordinates
- **Metadata retrieval**: Access detailed information about image products
- **Progressive loading**: Implement efficient multi-resolution image viewers

## Features

### 🔍 Search Images by Location
Search for HIRISE images near any location on Mars using latitude/longitude coordinates.

### 📊 Multi-Scale Tile Access
Access image pyramids at different scale levels (1x, 2x, 4x, 8x, etc.) for efficient browsing and viewing.

### 📝 Metadata Retrieval
Get detailed metadata including location, acquisition date, and product information.

### 🖼️ Image Download
Download and process images at any scale level using PIL/Pillow.

## Installation

### Requirements
```bash
pip install Pillow
```

No additional dependencies required - uses only Python standard library for HTTP requests.

## Quick Start

### Basic Usage

```python
from mars_hirise_api import HiriseAPI

# Initialize the API
api = HiriseAPI()

# Search for images near a location
results = api.search_images(
    latitude=18.65,      # Olympus Mons
    longitude=226.2,
    radius_km=100,
    limit=5
)

# Get multi-scale tiles for an image
product_id = "ESP_016644_1755"
tiles = api.get_multi_scale_tiles(product_id, scale_levels=[1, 2, 4, 8])

# Download image at a specific scale
image = api.get_image_at_scale(product_id, scale=8)
if image:
    image.show()
```

## API Reference

### HiriseAPI Class

#### `search_images(latitude, longitude, radius_km, limit)`
Search for HIRISE images by location.

**Parameters:**
- `latitude` (float): Center latitude (-90 to 90)
- `longitude` (float): Center longitude (0 to 360)
- `radius_km` (float): Search radius in kilometers
- `limit` (int): Maximum number of results (default: 10)

**Returns:** List of image metadata dictionaries

#### `get_image_metadata(product_id)`
Get detailed metadata for a specific image.

**Parameters:**
- `product_id` (str): HIRISE product ID (e.g., "ESP_012345_1234")

**Returns:** Dictionary containing image metadata

#### `get_multi_scale_tiles(product_id, scale_levels)`
Get URLs for multi-resolution image pyramid.

**Parameters:**
- `product_id` (str): HIRISE product ID
- `scale_levels` (list): Scale levels to fetch (e.g., [1, 2, 4, 8])

**Returns:** Dictionary mapping scale level to URL

#### `get_image_at_scale(product_id, scale)`
Download image at a specific scale level.

**Parameters:**
- `product_id` (str): HIRISE product ID
- `scale` (int): Scale level (1=full, 2=half, 4=quarter, etc.)

**Returns:** PIL Image object or None

#### `download_image(url, scale)`
Download and optionally resize an image.

**Parameters:**
- `url` (str): Image URL
- `scale` (float): Resize factor (1.0 = original size)

**Returns:** PIL Image object or None

#### `get_location_info(product_id)`
Get the center coordinates for an image.

**Parameters:**
- `product_id` (str): HIRISE product ID

**Returns:** Tuple of (latitude, longitude) or None

## Usage Examples

See `hirise_examples.py` for comprehensive examples including:

1. **Basic Search**: Find images by location
2. **Multi-Scale Tiles**: Access image pyramids
3. **Download Images**: Retrieve and process images
4. **Metadata**: Get detailed product information
5. **Complete Workflow**: End-to-end multi-scale imaging
6. **Custom Scaling**: Apply custom resize operations

Run the examples:
```bash
python hirise_examples.py
```

## Scale Levels Explained

Multi-scale imaging uses image pyramids for efficient viewing:

- **Scale 1**: Full resolution (largest file, highest detail)
- **Scale 2**: Half resolution (1/4 file size)
- **Scale 4**: Quarter resolution (1/16 file size)
- **Scale 8**: Eighth resolution (1/64 file size)
- **Scale 16**: Sixteenth resolution (1/256 file size)

### Use Cases by Scale:
- **Scale 8-16**: Initial preview, thumbnails
- **Scale 4**: Medium-detail browsing
- **Scale 2**: High-detail examination
- **Scale 1**: Maximum detail, scientific analysis

## Notable Mars Locations

Here are some interesting locations to explore:

| Feature | Latitude | Longitude | Description |
|---------|----------|-----------|-------------|
| Olympus Mons | 18.65 | 226.2 | Largest volcano in solar system |
| Valles Marineris | -13.9 | 301.3 | Massive canyon system |
| Gale Crater | -5.4 | 137.8 | Curiosity rover landing site |
| Jezero Crater | 18.4 | 77.5 | Perseverance rover landing site |
| Victoria Crater | -2.1 | 354.5 | Impact crater explored by Opportunity |

## Data Sources

This API interfaces with:
- **ODE REST API**: Orbital Data Explorer for search and metadata
- **HIRISE Image Server**: Public image repository at hirise.lpl.arizona.edu

## Technical Details

### Coordinate System
- Latitude: -90° (South) to +90° (North)
- Longitude: 0° to 360° (East)

### Image Formats
- Primary: JPEG for browse products
- Full scientific data available in PDS format through HIRISE website

### Network Requirements
- Internet connection required for API access
- Recommended timeout: 30s for metadata, 60s for images
- Large full-resolution images may take several minutes

## Integration with Existing Code

The HIRISE API can be integrated with the existing Mars guessing game:

```python
from mars_hirise_api import HiriseAPI

# In Mars_thinker.py, add HIRISE image support
api = HiriseAPI()

# Get HIRISE image for a location
def get_hirise_image_for_location(lat, lon):
    results = api.search_images(lat, lon, radius_km=50, limit=1)
    if results:
        product_id = results[0].get('pdsid')
        return api.get_image_at_scale(product_id, scale=4)
    return None
```

## Limitations

- Requires active internet connection
- API availability depends on ODE and HIRISE servers
- Not all Mars locations have HIRISE coverage
- Some product IDs in examples may not exist

## Contributing

This API can be extended to support:
- Additional Mars imaging instruments (CTX, MOC, etc.)
- Cached image downloads
- Async/parallel image fetching
- Advanced filtering (by acquisition date, quality, etc.)

## License

This API module follows the same license as the parent GuessTheWorld project.

## References

- [HIRISE Website](https://hirise.lpl.arizona.edu/)
- [ODE REST API Documentation](https://oderest.rsl.wustl.edu/)
- [Mars Reconnaissance Orbiter](https://mars.nasa.gov/mro/)
- [PDS Geosciences Node](https://pds-geosciences.wustl.edu/)

## Support

For issues or questions about this API module, please refer to the main repository issue tracker.
