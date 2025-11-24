"""
Multi-Planet Geoguesser Game

A planet-dependent geoguesser for Mercury, Mars, Venus, and Moon using
orbital data from NASA missions. Based on the Mars_thinker.py interface.

Features:
- Support for multiple planets (Mars, Moon, Venus, Mercury)
- Uses high-resolution orbital data (HIRISE, LRO, Magellan, MESSENGER)
- Random feature-based guessing game
- GUI interface with tkinter
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
import zipfile
import xml.etree.ElementTree as ET
import os
from typing import List, Tuple, Optional
from orbital_data_api import PlanetaryDataAPI, create_planet_metadata_dict


# Patch size for cropped images
PATCH_SIZE = 180


class PlanetGuessGame:
    """Multi-planet guessing game with GUI interface."""
    
    def __init__(self, master, planet: str = 'mars'):
        """
        Initialize the planet guessing game.
        
        Args:
            master: Tkinter master window
            planet: Planet name ('mars', 'moon', 'venus', 'mercury')
        """
        self.master = master
        self.planet = planet.lower()
        self.score = 0
        self.round = 0
        self.active = False
        
        # Load planet data
        self.load_planet_data()
        
        # Initialize API for this planet
        try:
            self.api = PlanetaryDataAPI(self.planet)
        except Exception as e:
            print(f"Warning: Could not initialize API for {self.planet}: {e}")
            self.api = None
        
        # Setup GUI
        self.setup_gui()
    
    def load_planet_data(self):
        """Load planet-specific map and nomenclature data."""
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        
        # Get planet metadata
        metadata = create_planet_metadata_dict(self.planet)
        self.planet_name = metadata.get('name', self.planet.capitalize())
        
        # Try to load planet map image
        map_file = os.path.join(data_dir, metadata.get('map_image', ''))
        if os.path.exists(map_file):
            self.planet_img = Image.open(map_file)
            self.width, self.height = self.planet_img.size
        else:
            # Create a placeholder image if map not available
            print(f"Warning: Map image not found for {self.planet}, using placeholder")
            self.planet_img = Image.new('RGB', (1024, 512), color=(100, 100, 100))
            self.width, self.height = self.planet_img.size
        
        # Try to load nomenclature data
        kmz_file = os.path.join(data_dir, metadata.get('nomenclature_file', ''))
        self.points = []
        
        if os.path.exists(kmz_file):
            try:
                self.points = self.load_kmz_points(kmz_file)
                print(f"Loaded {len(self.points)} features for {self.planet}")
            except Exception as e:
                print(f"Error loading nomenclature for {self.planet}: {e}")
        
        # If no points loaded, create some default ones for demonstration
        if not self.points:
            self.points = self.create_default_features()
    
    def load_kmz_points(self, kmz_file: str) -> List[Tuple[float, float, str]]:
        """
        Load feature points from KMZ file.
        
        Args:
            kmz_file: Path to KMZ file
            
        Returns:
            List of (lat, lon, name) tuples
        """
        points = []
        
        with zipfile.ZipFile(kmz_file, 'r') as z:
            kml_filename = [n for n in z.namelist() if n.endswith('.kml')][0]
            kml_data = z.read(kml_filename)
        
        root = ET.fromstring(kml_data)
        ns = {'kml': 'http://www.opengis.net/kml/2.2'}
        
        for pm in root.findall('.//kml:Placemark', ns):
            coords = pm.find('.//kml:coordinates', ns)
            name = pm.find('kml:name', ns)
            if coords is not None:
                lon, lat, *_ = map(float, coords.text.strip().split(','))
                # Convert -180:180 to 0:360 if needed
                lon = lon + 360 if lon < 0 else lon
                points.append((lat, lon, name.text if name is not None else ''))
        
        return points
    
    def create_default_features(self) -> List[Tuple[float, float, str]]:
        """Create default features for planets without KMZ data."""
        # Default features for each planet (lat, lon, name)
        default_features = {
            'mars': [
                (18.65, 226.2, 'Olympus Mons'),
                (-13.9, 301.3, 'Valles Marineris'),
                (-5.4, 137.8, 'Gale Crater'),
                (25.0, 315.0, 'Viking 1 Landing Site'),
            ],
            'moon': [
                (0.67, 23.47, 'Mare Tranquillitatis'),
                (-8.5, 15.5, 'Mare Nectaris'),
                (26.1, 3.2, 'Mare Imbrium'),
                (0.0, 0.0, 'Luna Center'),
            ],
            'venus': [
                (0.0, 0.0, 'Venus Center'),
                (65.0, 0.0, 'North Region'),
                (-65.0, 180.0, 'South Region'),
                (30.0, 90.0, 'East Region'),
            ],
            'mercury': [
                (0.0, 0.0, 'Mercury Center'),
                (30.0, 30.0, 'Caloris Basin'),
                (-30.0, 180.0, 'South Pole Region'),
                (45.0, 270.0, 'West Region'),
            ]
        }
        
        return default_features.get(self.planet, [(0.0, 0.0, 'Unknown Feature')])
    
    def setup_gui(self):
        """Setup the GUI elements."""
        # Title
        title = tk.Label(
            self.master, 
            text=f"{self.planet_name} Name-Guessing Game",
            font=("Helvetica", 16, "bold")
        )
        title.pack(pady=10)
        
        # Image display
        self.image_label = tk.Label(self.master)
        self.image_label.pack()
        
        # Entry field
        self.entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.entry.pack(pady=5)
        
        # Feedback label
        self.feedback = tk.Label(self.master, text="", font=("Helvetica", 12))
        self.feedback.pack()
        
        # Score label
        self.score_label = tk.Label(self.master, text="Score: 0", font=("Helvetica", 12))
        self.score_label.pack()
        
        # Button frame
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)
        
        # Start button
        self.start_button = tk.Button(
            button_frame, 
            text="Start", 
            command=self.start_game,
            font=("Helvetica", 10)
        )
        self.start_button.pack(side="left", padx=10)
        
        # Stop button
        self.stop_button = tk.Button(
            button_frame, 
            text="Stop", 
            command=self.stop_game,
            font=("Helvetica", 10)
        )
        self.stop_button.pack(side="right", padx=10)
        
        # Submit button
        self.submit_button = tk.Button(
            self.master, 
            text="Submit Guess", 
            command=self.check_guess,
            font=("Helvetica", 10)
        )
        self.submit_button.pack(pady=5)
    
    def start_game(self):
        """Start a new game."""
        if not self.points:
            self.feedback.config(
                text=f"No features available for {self.planet}. Please download data first."
            )
            return
        
        self.active = True
        self.score = 0
        self.round = 0
        self.score_label.config(text="Score: 0")
        self.next_round()
    
    def stop_game(self):
        """Stop the current game."""
        self.active = False
        self.feedback.config(text=f"Game stopped! Final Score: {self.score}")
    
    def next_round(self):
        """Start the next round of the game."""
        if not self.active:
            return
        
        self.round += 1
        self.feedback.config(text=f"Round {self.round}: Guess the feature!")
        
        # Pick a random feature
        self.target = random.choice(self.points)
        lat, lon, self.target_name = self.target
        
        # Convert lat/lon to pixel coordinates
        px = int((lon / 360) * self.width)
        py = int(((90 - lat) / 180) * self.height)
        
        # Crop patch
        left = max(px - PATCH_SIZE // 2, 0)
        upper = max(py - PATCH_SIZE // 2, 0)
        right = min(px + PATCH_SIZE // 2, self.width)
        lower = min(py + PATCH_SIZE // 2, self.height)
        
        patch = self.planet_img.crop((left, upper, right, lower))
        
        # Scale up for better visibility
        scale_factor = 2
        new_size = (PATCH_SIZE * scale_factor, PATCH_SIZE * scale_factor)
        patch_resized = patch.resize(new_size, Image.LANCZOS)
        
        self.tk_patch = ImageTk.PhotoImage(patch_resized)
        self.image_label.config(image=self.tk_patch)
        
        self.entry.delete(0, tk.END)
    
    def check_guess(self):
        """Check the player's guess."""
        if not self.active:
            return
        
        guess = self.entry.get().strip().lower()
        target_name_lower = self.target_name.lower()
        
        if guess == target_name_lower:
            self.feedback.config(text=f"Correct! It was {self.target_name} 🎉")
            self.score += 1
        else:
            self.feedback.config(text=f"Wrong! It was {self.target_name}")
        
        self.score_label.config(text=f"Score: {self.score}")
        
        # Move to next round after short delay
        self.master.after(1500, self.next_round)


class MultiPlanetSelector:
    """Main window with planet selection."""
    
    def __init__(self, master):
        """Initialize the multi-planet selector."""
        self.master = master
        self.master.title("Guess the World - Multi-Planet Geoguesser")
        self.master.geometry("900x900")
        
        # Title
        title = tk.Label(
            master,
            text="Guess the World",
            font=("Helvetica", 20, "bold")
        )
        title.pack(pady=20)
        
        # Subtitle
        subtitle = tk.Label(
            master,
            text="Select a planet to begin:",
            font=("Helvetica", 14)
        )
        subtitle.pack(pady=10)
        
        # Planet selection frame
        planet_frame = tk.Frame(master)
        planet_frame.pack(pady=20)
        
        # Create buttons for each planet
        planets = [
            ('Mars', 'mars', 'HIRISE'),
            ('Moon', 'moon', 'LRO'),
            ('Venus', 'venus', 'Magellan'),
            ('Mercury', 'mercury', 'MESSENGER')
        ]
        
        for i, (name, planet_id, mission) in enumerate(planets):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(
                planet_frame,
                text=f"{name}\n({mission})",
                command=lambda p=planet_id: self.start_planet_game(p),
                font=("Helvetica", 12),
                width=15,
                height=3
            )
            btn.grid(row=row, column=col, padx=10, pady=10)
        
        # Info label
        info = tk.Label(
            master,
            text="Using orbital data from NASA missions",
            font=("Helvetica", 10),
            fg="gray"
        )
        info.pack(pady=10)
    
    def start_planet_game(self, planet: str):
        """Start a game for the selected planet."""
        # Create new window for the game
        game_window = tk.Toplevel(self.master)
        game_window.title(f"Guess the World - {planet.capitalize()}")
        game_window.geometry("800x800")
        
        # Create and run the game
        game = PlanetGuessGame(game_window, planet)


def main():
    """Main entry point for the multi-planet geoguesser."""
    root = tk.Tk()
    app = MultiPlanetSelector(root)
    root.mainloop()


if __name__ == "__main__":
    main()
