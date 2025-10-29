import sys
import json
from urllib import parse, request

#
# This script takes a quoted string on the command line and hits
# the Nominatim service to assign geocoordinates (ie, latitude and
# longitude) to the string.
#
# Generally speaking, the affiliation string you'd get from a 
# publication will NOT work as is, so I wrote a wrapper
# script (location_munger.pl) that will strip off the beginning
# of the location string up to the first comma and try again,
# iteratively, until nothing is left. 
#
# IMPORTANT NOTE: if you use this script be aware that the service 
# is limited to the number of times it can be accesses. I believe the
# limit is one per second, but to be safe, it generally make it a 
# sleep of 5 or 10 seconds between requests.
#


def geocode_location(location_string):
    """Geocode a location using Nominatim (OpenStreetMap)"""
    
    if not location_string.strip():
        print("Error: Empty location string")
        return None
    
    # Build the API URL
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={parse.quote(location_string)}&limit=1"
    
    try:
        # Add User-Agent header (required by Nominatim)
        req = request.Request(url, headers={'User-Agent': 'Institution Geocoder Script'})
        
        with request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            if data and len(data) > 0:
                result = data[0]
                lat = float(result['lat'])
                lon = float(result['lon'])
                display_name = result.get('display_name', '')
                
                # Print to stdout in a structured format
                print(f"SUCCESS")
                print(f"Latitude: {lat}")
                print(f"Longitude: {lon}")
                print(f"Display Name: {display_name}")
                print(f"Coordinates: {lat},{lon}")
                
                return {'lat': lat, 'lon': lon, 'display_name': display_name}
            else:
                print("FAILED: No results found")
                return None
                
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return None

def main():
    # Check if location was provided as argument
    if len(sys.argv) < 2:
        print("Usage: python geocode_single.py \"location string\"")
        print("Example: python geocode_single.py \"Paris, France\"")
        print("Example: python geocode_single.py \"Harvard University, Cambridge, MA, USA\"")
        sys.exit(1)
    
    # Get location from command line argument
    location = " ".join(sys.argv[1:])
    
    print(f"Geocoding: {location}")
    print("-" * 60)
    
    geocode_location(location)

if __name__ == "__main__":
    main()
