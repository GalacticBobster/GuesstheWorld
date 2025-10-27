import requests
from PIL import Image
from io import BytesIO
import zipfile
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

# --- Step 1: Fetch Mars Viking mosaic directly from USGS PDS ---
url = "https://astrogeology.usgs.gov/download/MARS/VIKING_CLRMOSAIC/global_1024.jpg"
response = requests.get(url)
mars_img = Image.open(BytesIO(response.content))

# --- Step 2: Extract coordinates from KMZ ---
kmz_file = '../data/MARS_nomenclature_center_pts.kmz'

with zipfile.ZipFile(kmz_file, 'r') as z:
    kml_filename = [n for n in z.namelist() if n.endswith('.kml')][0]
    kml_data = z.read(kml_filename)

root = ET.fromstring(kml_data)
ns = {'kml': 'http://www.opengis.net/kml/2.2'}

lons, lats, names = [], [], []

for pm in root.findall('.//kml:Placemark', ns):
    coords = pm.find('.//kml:coordinates', ns)
    name = pm.find('kml:name', ns)
    if coords is not None:
        lon, lat, *_ = map(float, coords.text.strip().split(','))
        # Convert -180:180 to 0:360 for the Viking mosaic
        lon = lon + 360 if lon < 0 else lon
        lons.append(lon)
        lats.append(lat)
        names.append(name.text if name is not None else '')

# --- Step 3: Plot Mars image and overlay points ---
plt.figure(figsize=(12,6))
plt.imshow(mars_img, extent=[0, 360, -90, 90])
plt.scatter(lons, lats, c='red', s=5, label='Named features')

# Optional: label a subset of features
for i in range(0, len(names), max(1, len(names)//20)):
    plt.text(lons[i], lats[i], names[i], fontsize=5, color='yellow')

plt.xlabel('Longitude (°E)')
plt.ylabel('Latitude (°N)')
plt.title('Mars Named Features on Viking Mosaic')
plt.grid(True)
plt.legend()
plt.savefig('mars_features_automated.png', dpi=300)
plt.show()

