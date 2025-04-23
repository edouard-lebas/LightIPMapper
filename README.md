# LightIPMapper
Analyzes files to extract and map IP addresses

## Features

- Extracts public IP addresses from files.
- Locates IP addresses using the GeoIP database.
- Creates an interactive map with markers for the located IPs.
- Markers are color-coded based on the number of requests.
- Unlocated IPs are marked in gray and set to "Grande Terre".
- Supports different layers for high, medium, low, top 10 requests, and unlocated IPs.

# Pre-requisite
- Add your Maxmind GeoLiteCity.dat in "./db"

## Usage

To run the program:

```sh
python main.py -d .\in\
