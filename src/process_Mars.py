import zipfile
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

kmz_file = '../data/MARS_nomenclature_center_pts.kmz'


lons, lats, names = [], [], []
with zipfile.ZipFile(kmz_file, 'r') as z:
    kml_filename = [n for n in z.namelist() if n.endswith('.kml')][0]
    kml_data = z.read(kml_filename)

# Step 2 — Parse KML
root = ET.fromstring(kml_data)
ns = {'kml': 'http://www.opengis.net/kml/2.2'}


for pm in root.findall('.//kml:Placemark', ns):
    coords = pm.find('.//kml:coordinates', ns)
    name = pm.find('kml:name', ns)
    if coords is not None:
        lon, lat, *_ = map(float, coords.text.strip().split(','))
        lons.append(lon)
        lats.append(lat)
        names.append(name.text if name is not None else '')

img = mpimg.imread('../data/mars_viking_clrmosaic_global_1024.jpg')

#plt.figure(figsize=(12,6))
# Assuming the image covers 0-360°E longitude, -90° to 90° latitude
#plt.imshow(img, extent=[0, 360, -90, 90])


# Step 3 — Plot
plt.figure(figsize=(8, 4))
plt.scatter(lons, lats, s=5, color='red')
plt.imshow(img, extent=[-180, 180, -90, 90])
plt.title('Mars Named Features (KML)')
plt.xlabel('Longitude (°E)')
plt.ylabel('Latitude (°N)')
plt.grid(True)

# Optional: annotate a few feature names
for i in range(0, len(names), max(1, len(names)//20)):
    plt.text(lons[i], lats[i], names[i], fontsize=6)

# Step 4 — Save
plt.savefig('mars_features.png', dpi=300)
plt.show()
