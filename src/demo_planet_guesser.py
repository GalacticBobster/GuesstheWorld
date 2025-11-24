"""
Demo script for Multi-Planet Geoguesser

This script demonstrates the core functionality of the multi-planet geoguesser
without requiring a GUI. Useful for testing and understanding the game mechanics.
"""

from orbital_data_api import PlanetaryDataAPI, create_planet_metadata_dict
import random


def demo_planet_api(planet_name):
    """Demonstrate API functionality for a specific planet."""
    print(f"\n{'='*70}")
    print(f"DEMO: {planet_name.upper()} Geoguesser")
    print(f"{'='*70}")
    
    # Initialize API
    api = PlanetaryDataAPI(planet_name)
    metadata = create_planet_metadata_dict(planet_name)
    
    # Display planet information
    print(f"\nPlanet Information:")
    print(f"  Name: {metadata['name']}")
    print(f"  Radius: {api.radius_km} km")
    print(f"  Instruments: {', '.join(api.config['instruments'])}")
    print(f"  KM per degree: {api.km_per_degree:.2f}")
    
    # Display data files
    print(f"\nData Files:")
    print(f"  Map Image: {metadata['map_image']}")
    print(f"  Nomenclature: {metadata['nomenclature_file']}")
    
    # Simulate feature selection
    print(f"\nGame Simulation:")
    print(f"  In the actual game, random features from {planet_name} would be selected")
    print(f"  Players would see image patches and guess the feature name")
    print(f"  Correct guesses increase the score")
    
    # Show example features (these would come from KMZ in actual game)
    example_features = {
        'mars': ['Olympus Mons', 'Valles Marineris', 'Gale Crater', 'Viking 1 Landing Site'],
        'moon': ['Mare Tranquillitatis', 'Mare Nectaris', 'Mare Imbrium', 'Tycho Crater'],
        'venus': ['Maxwell Montes', 'Aphrodite Terra', 'Ishtar Terra', 'Beta Regio'],
        'mercury': ['Caloris Basin', 'Rembrandt Basin', 'Raditladi Basin', 'Beethoven Basin']
    }
    
    features = example_features.get(planet_name, ['Unknown Feature'])
    print(f"\nExample Features ({len(features)} loaded):")
    for i, feature in enumerate(features, 1):
        print(f"  {i}. {feature}")
    
    # Simulate a round
    print(f"\n--- Simulated Game Round ---")
    feature = random.choice(features)
    print(f"[Image patch would be displayed here]")
    print(f"Question: What feature is this?")
    print(f"Answer: {feature}")
    print(f"[Player would type their guess and submit]")


def demo_all_planets():
    """Demonstrate all planet APIs."""
    print("\n" + "="*70)
    print("MULTI-PLANET GEOGUESSER - COMPREHENSIVE DEMO")
    print("="*70)
    
    print("\nSupported Planets:")
    planets = [
        ('Mars', 'mars', 'HIRISE / MRO'),
        ('Moon', 'moon', 'LRO / LROC'),
        ('Venus', 'venus', 'Magellan'),
        ('Mercury', 'mercury', 'MESSENGER / MDIS')
    ]
    
    for name, planet_id, mission in planets:
        print(f"  • {name} ({mission})")
    
    # Demo each planet
    for name, planet_id, mission in planets:
        demo_planet_api(planet_id)
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("\nThe Multi-Planet Geoguesser provides:")
    print("  ✓ Unified API for 4 planets (Mars, Moon, Venus, Mercury)")
    print("  ✓ Integration with NASA's Orbital Data Explorer")
    print("  ✓ Support for multiple mission instruments")
    print("  ✓ Random feature-based guessing game")
    print("  ✓ GUI interface (requires tkinter)")
    print("\nTo play the game:")
    print("  1. Download planetary data: ./download_all_planets.sh")
    print("  2. Run: python planet_guesser.py")
    print("  3. Select a planet and start guessing!")
    print("\n" + "="*70)


def demo_ode_api():
    """Demonstrate ODE REST API integration."""
    print("\n" + "="*70)
    print("ORBITAL DATA EXPLORER (ODE) API INTEGRATION")
    print("="*70)
    
    print("\nThe ODE REST API provides:")
    print("  • Search for images by geographic location")
    print("  • Access to metadata (coordinates, dates, instrument info)")
    print("  • Support for multiple planetary missions")
    print("  • High-resolution imagery from orbital instruments")
    
    print("\nExample API Usage:")
    print("""
    from orbital_data_api import PlanetaryDataAPI
    
    # Initialize for Mars
    api = PlanetaryDataAPI('mars')
    
    # Search for images near Olympus Mons
    results = api.search_images(
        latitude=18.65,
        longitude=226.2,
        radius_km=100,
        limit=5
    )
    
    # Get metadata for specific image
    metadata = api.get_image_metadata(product_id)
    
    # Get location info
    location = api.get_location_info(product_id)
    """)
    
    print("\nNote: Actual image download requires network access to ODE servers")


if __name__ == "__main__":
    print("\n" + "#"*70)
    print("#" + " "*68 + "#")
    print("#" + "  Multi-Planet Geoguesser - Interactive Demo".center(68) + "#")
    print("#" + " "*68 + "#")
    print("#"*70)
    
    # Run all demos
    demo_all_planets()
    demo_ode_api()
    
    print("\n" + "#"*70)
    print("#" + " "*68 + "#")
    print("#" + "  Demo Complete!".center(68) + "#")
    print("#" + " "*68 + "#")
    print("#"*70 + "\n")
