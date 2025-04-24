# LightIPMapper
Analyzes files to extract and map IP addresses

## Features

- Extracts public IP addresses from files.
- Locates IP addresses using the GeoIP database.
- Creates an interactive map with markers for the located IPs.
- Markers are color-coded based on the number of requests.
- Unlocated IPs are marked in gray and set to "Grande Terre".
- Supports different layers for high, medium, low, top 10 requests, and unlocated IPs.


## Usage
- Add your Maxmind GeoLiteCity.dat in "./db"
- Upload your source files to ./in/

```sh
pip install -r requirements.txt
python main.py -d .\in\
