# GuesstheWorld
A multi-planet geoguesser game using orbital data from NASA missions

## Overview
GuesstheWorld is an interactive guessing game that challenges players to identify features on different celestial bodies in our solar system. Using high-resolution orbital imagery from various NASA missions, players are shown random patches of planetary surfaces and must guess which named feature they're looking at.

## Supported Planets

### Mars - HIRISE Mission
- **Mission**: Mars Reconnaissance Orbiter (MRO) - High Resolution Imaging Science Experiment
- **Data Source**: HIRISE browse images via ODE REST API
- **Features**: Named craters, mountains, valleys, and landing sites from Mars nomenclature

### Moon - LRO Mission
- **Mission**: Lunar Reconnaissance Orbiter (LRO)
- **Data Source**: LROC (Lunar Reconnaissance Orbiter Camera) images
- **Features**: Lunar maria, craters, and historic landing sites

### Venus - Magellan Mission
- **Mission**: Magellan Radar Mapping Mission
- **Data Source**: Magellan radar imagery
- **Features**: Venusian surface features mapped by radar

### Mercury - MESSENGER Mission
- **Mission**: MESSENGER (MErcury Surface, Space ENvironment, GEochemistry, and Ranging)
- **Data Source**: MDIS (Mercury Dual Imaging System) images
- **Features**: Mercurian craters and geological features

## Installation

### Prerequisites
- Python 3.6+
- Required packages: Pillow (PIL)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/GalacticBobster/GuesstheWorld.git
cd GuesstheWorld
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download planetary data:
```bash
cd src
chmod +x download_all_planets.sh
./download_all_planets.sh
```

This will download:
- Global map images for Mars, Moon, Venus, and Mercury
- Nomenclature center points (KMZ files) for each planet

## Usage

### Multi-Planet Geoguesser (Recommended)
Run the main multi-planet game that allows you to select which planet to play:

```bash
cd src
python planet_guesser.py
```

This will open a GUI where you can:
1. Select a planet (Mars, Moon, Venus, or Mercury)
2. Start a guessing game for that planet
3. Try to identify features from randomly shown image patches
4. Track your score across multiple rounds

### Mars-Specific Game (Original)
The original Mars-only game is still available:

```bash
cd src
python Mars_thinker.py
```

## How to Play

1. **Start the Game**: Launch `planet_guesser.py` and select a planet
2. **View the Image**: A random patch from the planet's surface will be displayed
3. **Make Your Guess**: Type the name of the feature you think is shown
4. **Submit**: Click "Submit Guess" to check your answer
5. **Score**: Correct guesses increase your score
6. **Continue**: The game automatically advances to the next round

## Features

### Multi-Planet Support
- Unified interface for all four planets
- Planet-specific data and nomenclature
- Seamless switching between different celestial bodies

### Orbital Data Integration
- **ODE REST API**: Integration with NASA's Orbital Data Explorer
- **High-Resolution Images**: Access to mission-specific imagery
- **Metadata Access**: Feature locations, coordinates, and descriptions

### Game Mechanics
- Random feature selection from official nomenclature
- Progressive difficulty with diverse feature types
- Score tracking and feedback
- Clean, intuitive GUI interface

## API Documentation

### Orbital Data Explorer API
The `orbital_data_api.py` module provides a unified interface for accessing planetary data:

```python
from orbital_data_api import PlanetaryDataAPI

# Initialize API for a specific planet
api = PlanetaryDataAPI('mars')  # or 'moon', 'venus', 'mercury'

# Search for images by location
results = api.search_images(latitude=18.65, longitude=226.2, radius_km=100)

# Get metadata for specific features
metadata = api.get_image_metadata(product_id)
```

### Mars HIRISE API (Legacy)
The original Mars-specific API is available in `mars_hirise_api.py`:

```python
from mars_hirise_api import HiriseAPI

api = HiriseAPI()
results = api.search_images(latitude=18.65, longitude=226.2, radius_km=100)
```

## Project Structure

```
GuesstheWorld/
├── src/
│   ├── planet_guesser.py          # Multi-planet game (NEW)
│   ├── orbital_data_api.py        # Unified planetary API (NEW)
│   ├── Mars_thinker.py            # Original Mars game
│   ├── mars_hirise_api.py         # Mars-specific API
│   ├── download_all_planets.sh   # Data download script (NEW)
│   └── download_planetData.sh    # Mars data download (original)
├── data/                          # Planetary maps and nomenclature (created by scripts)
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Data Sources

All data is sourced from official NASA and USGS repositories:
- **Planetary Nomenclature**: IAU Gazetteer of Planetary Nomenclature (via AWS S3)
- **Mars Images**: USGS Astrogeology, HiRISE/MRO mission
- **Moon Images**: LROC/LRO mission data
- **Venus Images**: Magellan mission radar data
- **Mercury Images**: MESSENGER/MDIS mission data

## Contributing

Contributions are welcome! Feel free to:
- Add support for additional planets or moons
- Improve the game interface
- Add new features or game modes
- Fix bugs or improve documentation

## License

See LICENSE file for details.

## Acknowledgments

- NASA for providing open access to planetary data
- Mars Reconnaissance Orbiter (MRO) team
- Lunar Reconnaissance Orbiter (LRO) team  
- Magellan mission team
- MESSENGER mission team
- USGS Astrogeology Science Center
- IAU Working Group for Planetary System Nomenclature
