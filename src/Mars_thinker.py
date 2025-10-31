import tkinter as tk
from PIL import Image, ImageTk
import random
import zipfile
import xml.etree.ElementTree as ET
import base64

# --- Load Mars image and KMZ points ---
mars_img = Image.open('../data/mars_viking_clrmosaic_global_1024.jpg')
width, height = mars_img.size

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


# points = list of tuples: (lat, lon, name)
# e.g., points = [(lat1, lon1, "Feature1"), (lat2, lon2, "Feature2"), ...]

# Patch size
PATCH_SIZE = 180

class MarsGuessGame:
    def __init__(self, master, mars_img, points):
        self.master = master
        self.mars_img = mars_img
        self.points = points
        self.score = 0
        self.round = 0
        self.active = False

        # GUI elements
        self.image_label = tk.Label(master)
        self.image_label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.feedback = tk.Label(master, text="", font=("Helvetica", 12))
        self.feedback.pack()

        self.score_label = tk.Label(master, text="Score: 0", font=("Helvetica", 12))
        self.score_label.pack()

        self.start_button = tk.Button(master, text="Start", command=self.start_game)
        self.start_button.pack(side="left", padx=10, pady=10)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_game)
        self.stop_button.pack(side="right", padx=10, pady=10)

        self.submit_button = tk.Button(master, text="Submit Guess", command=self.check_guess)
        self.submit_button.pack(pady=5)

    def start_game(self):
        self.active = True
        self.score = 0
        self.round = 0
        self.score_label.config(text="Score: 0")
        self.next_round()

    def stop_game(self):
        self.active = False
        self.feedback.config(text=f"Game stopped! Final Score: {self.score}")

    def next_round(self):
        if not self.active:
            return

        self.round += 1
        self.feedback.config(text=f"Round {self.round}: Guess the feature!")

        # Pick a random feature
        self.target = random.choice(self.points)
        lat, lon, self.target_name = self.target

        # Convert lat/lon to pixel coordinates
        px = int((lon / 360) * width)
        py = int(((90 - lat) / 180) * height)

        # Crop patch
        left = max(px - PATCH_SIZE // 2, 0)
        upper = max(py - PATCH_SIZE // 2, 0)
        right = min(px + PATCH_SIZE // 2, width)
        lower = min(py + PATCH_SIZE // 2, height)

        patch = self.mars_img.crop((left, upper, right, lower))
        scale_factor = 2  # e.g., 4x bigger
        new_size = (PATCH_SIZE * scale_factor, PATCH_SIZE * scale_factor)
        patch_resized = patch.resize(new_size, Image.NEAREST)

        self.tk_patch = ImageTk.PhotoImage(patch_resized)
        self.image_label.config(image=self.tk_patch)

        self.entry.delete(0, tk.END)

    def check_guess(self):
        if not self.active:
            return
        guess = self.entry.get().strip().lower()
        if guess == self.target_name.lower():
            self.feedback.config(text=f"Correct! It was {self.target_name} 🎉")
            self.score += 1
        else:
            self.feedback.config(text=f"Wrong! It was {self.target_name}")
        self.score_label.config(text=f"Score: {self.score}")

        # Move to next round after short delay
        self.master.after(1000, self.next_round)

# --- Run the GUI ---
root = tk.Tk()
root.title("Mars Name-Guessing Game")
root.geometry("800x800")
game = MarsGuessGame(root, mars_img, points)

root.mainloop()

