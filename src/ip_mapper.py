from datetime import datetime

import folium
from folium.plugins import MarkerCluster

from src.utils import GREEN, ENDC

# Coordinates for "Grande Terre"
GRANDE_TERRE_LATITUDE = -49.312136
GRANDE_TERRE_LONGITUDE = 69.108422


class IpMapper:
    def __init__(self, ip_locations, unlocated_ips):
        """
        Initializes the IpMapper with the located IPs and unlocated IPs.
        """
        self.ip_locations = ip_locations
        self.unlocated_ips = unlocated_ips

    def create_map(self):
        """
        Creates an interactive map with markers for the located IPs.
        Markers are color-coded based on the number of requests.
        Unlocated IPs are marked in gray and set to "Grande Terre".
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_file = f'.\out\\lightipmapper_{timestamp}.html'
        m = folium.Map(location=[20, 0], zoom_start=2)

        # Sort IPs by request count
        sorted_ips = sorted(self.ip_locations.items(), key=lambda x: x[1]['count'])
        total_ips = len(sorted_ips)
        top_15_percent = int(0.15 * total_ips)
        bottom_15_percent = int(0.15 * total_ips)
        top_10_ips = sorted_ips[-10:]

        # Create marker clusters for different layers
        top_10_requests_cluster = MarkerCluster(name='Top 10 Requests').add_to(m)
        high_requests_cluster = MarkerCluster(name='High Requests').add_to(m)
        medium_requests_cluster = MarkerCluster(name='Medium Requests').add_to(m)
        low_requests_cluster = MarkerCluster(name='Low Requests').add_to(m)
        unlocated_ips_cluster = MarkerCluster(name='Unlocated IPs').add_to(m)

        # Add markers to the appropriate clusters
        for i, (ip, data) in enumerate(sorted_ips):
            if i < bottom_15_percent:
                folium.Marker(
                    location=[data['latitude'], data['longitude']],
                    popup=f"IP: {ip} Requests: {data['count']}",
                    icon=folium.Icon(color='green')
                ).add_to(low_requests_cluster)
            elif i >= total_ips - top_15_percent:
                folium.Marker(
                    location=[data['latitude'], data['longitude']],
                    popup=f"IP: {ip} Requests: {data['count']}",
                    icon=folium.Icon(color='red')
                ).add_to(high_requests_cluster)
            else:
                folium.Marker(
                    location=[data['latitude'], data['longitude']],
                    popup=f"IP: {ip} Requests: {data['count']}",
                    icon=folium.Icon(color='orange')
                ).add_to(medium_requests_cluster)

        # Add top 10 requests to a separate cluster
        for ip, data in top_10_ips:
            folium.Marker(
                location=[data['latitude'], data['longitude']],
                popup=f"IP: {ip} Requests: {data['count']}",
                icon=folium.Icon(color='black')
            ).add_to(top_10_requests_cluster)

        # Add unlocated IPs to a separate cluster
        for ip, count in self.unlocated_ips:
            folium.Marker(
                location=[GRANDE_TERRE_LATITUDE, GRANDE_TERRE_LONGITUDE],
                popup=f"IP: {ip} Requests: {count}",
                icon=folium.Icon(color='gray')
            ).add_to(unlocated_ips_cluster)

        # Add layer control to the map
        folium.LayerControl().add_to(m)

        m.save(output_file)
        print(f"{GREEN}🗺️ Map saved to {output_file}{ENDC}")
