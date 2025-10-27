import zipfile
import xml.etree.ElementTree as ET
import folium
import base64
from folium.raster_layers import ImageOverlay
from folium.plugins import FloatImage
from PIL import Image
import cartopy.crs as ccrs

# --- Step 1: Extract KMZ coordinates ---
kmz_file = '../data/MARS_nomenclature_center_pts.kmz'
with zipfile.ZipFile(kmz_file, 'r') as z:
    kml_filename = [n for n in z.namelist() if n.endswith('.kml')][0]
    kml_data = z.read(kml_filename)

root = ET.fromstring(kml_data)
ns = {'kml': 'http://www.opengis.net/kml/2.2'}

points = []
for pm in root.findall('.//kml:Placemark', ns):
    coords = pm.find('.//kml:coordinates', ns)
    name = pm.find('kml:name', ns)
    if coords is not None:
        lon, lat, *_ = map(float, coords.text.strip().split(','))
        # Convert -180:180 to 0:360 for Folium if needed
        lon = lon + 360 if lon < 0 else lon
        points.append((lat, lon, name.text if name is not None else ''))

# --- Step 2: Load Mars basemap image ---
mars_img = '../data/mars_viking_clrmosaic_global_1024.jpg'
img = Image.open(mars_img)
width, height = img.size

# Extent: full globe, lon 0-360, lat -90 to 90
bounds = [[-90, 0], [90, 360]]

# --- Step 3: Create Folium map ---
m = folium.Map(location=[0, 180], zoom_start=2, tiles=None, crs='EPSG3857')

# Add Mars image as overlay
img_overlay = ImageOverlay(
    image=mars_img,
    bounds=bounds,
    opacity=1,
    interactive=True,
    cross_origin=False
)
img_overlay.add_to(m)

# --- Step 4: Add KMZ points as markers ---
for lat, lon, name in points:
    folium.CircleMarker(
        location=[lat, lon],
        radius=3,
        color='red',
        fill=True,
        fill_color='red',
        popup=name
    ).add_to(m)

# --- Step 5: Save map to HTML ---
m.save('mars_interactive_map.html')

