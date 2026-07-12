import os
import sys
import time
import math
from datetime import datetime
import requests

# 1. THE MAIN CONTROLLER
def main_dashboard():
    """Renders the actual visual user interface in a loop."""
    print("Querying NASA networks and tracking satellites...")
    iss_lat, iss_lon, ast_count, ast_name, ast_dist = fetch_space_data()
    
    frame = 0
    try:
        while True:
            clear_screen()
            draw_header()
            
            # --- COMPONENT 1: ISS LIVE MONITOR ---
            print("[COMPONENT: SAT_TRACKER]")
            print(f"Satellite Identity : International Space Station (ISS)")
            print(f"Current Coordinates: Latitude {iss_lat} / Longitude {iss_lon}")
            print("-" * 65)
            
            # --- COMPONENT 2: ASTEROID DEFENSE RADAR ---
            print("[COMPONENT: ASTEROID_RADAR]")
            print(f"Objects Tracked Today : {ast_count}")
            if ast_count > 0:
                print(f"Closest Flyby Object : {ast_name}")
                print(f"Miss Distance       : {ast_dist:,.1f} km away from Earth")
            else:
                print("Radar Status        : Deep space sectors clear")
            print("-" * 65)
            
            # --- COMPONENT 3: SIMULATED HARDWARE WAVE ---
            print("[HARDWARE WAVEFORM SIMULATOR]")
            wave_chars = [" ", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
            wave_string = ""
            for x in range(50):
                sine_val = math.sin((x / 5.0) + (frame / 2.0))
                index = int((sine_val + 1) * 3.5)
                wave_string += wave_chars[index]
            
            print(f"    Signal Stream: {wave_string}")
            print("=" * 65)
            print("Press [CTRL + C] in your terminal to safely shut down.")
            
            frame += 1
            time.sleep(0.1)
            
            # Every 150 frames (15 seconds), refresh the live data from NASA
            if frame % 150 == 0:
                iss_lat, iss_lon, ast_count, ast_name, ast_dist = fetch_space_data()
                
    except KeyboardInterrupt:
        print("\nDashboard shutdown sequence complete. Goodbye, Commander.")

# 2. SUB-FUNCTIONS & UTILITIES
def clear_screen():
    """Uses the 'os' library to cleanly wipe the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_header():
    """Prints a styled retro command center banner."""
    print("=" * 65)
    print("NASA MAIN TERMINAL DASHBOARD // SYSTEM STATE: ONLINE")
    print("=" * 65)
    print(f"SYSTEM TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 65)

def fetch_space_data():
    """Gathers real-time telemetry using public data APIs."""
    iss_lat, iss_lon = "Unknown", "Unknown"
    asteroid_count = 0
    closest_name = "None"
    closest_dist = float('inf')

    # Fetch Live ISS Data (Extended 10s timeout)
    try:
        iss_res = requests.get("http://opennotify.org", timeout=10).json()
        iss_lat = iss_res["iss_position"]["latitude"]
        iss_lon = iss_res["iss_position"]["longitude"]
    except Exception:
        pass

    # Fetch NASA Asteroid Data (Extended 10s timeout)
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        url = "https://nasa.gov"
        params = {"start_date": today, "end_date": today, "api_key": "DEMO_KEY"}
        neo_data = requests.get(url, params=params, timeout=10).json()
        
        asteroid_count = neo_data.get("element_count", 0)
        asteroids = neo_data.get("near_earth_objects", {}).get(today, [])
        
        for ast in asteroids:
            # Using your array location fix to look up close approach metadata
            dist = float(ast["close_approach_data"][0]["miss_distance"]["kilometers"])
            if dist < closest_dist:
                closest_dist = dist
                closest_name = ast["name"]
    except Exception:
        pass

    return iss_lat, iss_lon, asteroid_count, closest_name, closest_dist

# 3. BOOT ENGINE
if __name__ == "__main__":
    main_dashboard()
