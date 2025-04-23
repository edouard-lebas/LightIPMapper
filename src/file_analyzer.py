import ipaddress
import os
import re
from collections import Counter
from src.utils import YELLOW, ENDC, RED, BLUE, GREEN

import pygeoip


class FileAnalyzer:
    def __init__(self, file_paths):
        """
        Initializes the FileAnalyzer with a list of file paths and sets up the GeoIP database.
        """
        self.unlocated_ips = None
        self.ip_locations = None
        self.file_paths = file_paths
        self.ip_counter = Counter()
        self.geoip = pygeoip.GeoIP('db\\GeoLiteCity.dat')

    def extract_ips(self):
        """
        Extracts valid public IP addresses from the files and counts their occurrences.
        """
        # Improved IP pattern to ensure valid IP addresses
        ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

        for file_path in self.file_paths:
            try:
                if not os.path.isfile(file_path):
                    print(f"{RED}❌ The provided path is not a file: {file_path}{ENDC}")
                    continue

                print(f"{BLUE}🔍 Analyzing file: {file_path}{ENDC}")

                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    ips = ip_pattern.findall(content)
                    for ip in ips:
                        # Skip IPs containing ".0.0.0"
                        if ".0.0.0" in ip:
                            continue
                        try:
                            # Validate if the IP is a valid IPv4 address
                            ip_obj = ipaddress.IPv4Address(ip)
                            if not ip_obj.is_private:
                                self.ip_counter[ip] += 1
                        except ipaddress.AddressValueError:
                            pass

            except Exception as e:
                print(f"{RED}❌ An error occurred while processing {file_path}: {e}{ENDC}")

        print(f"{GREEN}✅ Total IPs extracted: {len(self.ip_counter)}{ENDC}")

    def locate_ips(self):
        """
        Locates the extracted IP addresses using the GeoIP database.
        IPs that cannot be located are set to "Grande Terre".
        """
        self.ip_locations = {}
        self.unlocated_ips = []
        for ip, count in self.ip_counter.items():
            match = self.geoip.record_by_addr(ip)
            if match is not None:
                self.ip_locations[ip] = {
                    'latitude': match['latitude'],
                    'longitude': match['longitude'],
                    'count': count
                }
            else:
                print(f"{YELLOW}⚠️ Could not locate IP: {ip}. Setting to Grande Terre.{ENDC}")
                self.unlocated_ips.append((ip, count))

        print(f"{GREEN}✅ Total IPs located: {len(self.ip_locations)}{ENDC}")
