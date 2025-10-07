import io
import folium
from PySide6.QtGui import QDesktopServices
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView

class WebEnginePage(QWebEnginePage):
    """Custom QWebEnginePage to open links in the external browser."""
    def acceptNavigationRequest(self, url, nav_type, is_main_frame):
        # Check if the link was clicked by the user
        if nav_type == QWebEnginePage.NavigationType.NavigationTypeLinkClicked:
            QDesktopServices.openUrl(url)  # Open in the system's default browser
            return False  # Tell the QWebEngineView to NOT navigate
        # Allow all other navigation requests
        return super().acceptNavigationRequest(url, nav_type, is_main_frame)

class MapWorker:
    """Manages all operations related to the Folium map."""
    def __init__(self, map_view_widget: QWebEngineView):
        if not map_view_widget:
            raise ValueError("A QWebEngineView widget must be provided.")
        
        self.map_view = map_view_widget
        
        # Set up the custom page to handle external link clicks
        custom_page = WebEnginePage(self.map_view)
        self.map_view.setPage(custom_page)

    def update_map(self, latitude, longitude):
        """Generates and displays a map for the given coordinates."""
        try:
            # Convert to float for Folium, handle potential errors
            lat = float(latitude)
            lon = float(longitude)
            coords = [lat, lon]
        except (ValueError, TypeError):
            # If coordinates are invalid, show a default location (e.g., Jakarta)
            print("Invalid coordinates provided. Showing default map.")
            coords = [-6.2088, 106.8456]

        # Create the map
        m = folium.Map(location=coords, zoom_start=16)

        # Create the Google Maps URL and popup HTML
        gmaps_url = f"https://www.google.com/maps/search/?api=1&query={coords[0]},{coords[1]}"
        popup_html = f'<a href="{gmaps_url}" target="_blank">Open in Google Maps</a>'

        # Add a marker to the map
        folium.Marker(
            location=coords,
            popup=popup_html,
            tooltip="Click for options"
        ).add_to(m)

        # Save map data to an in-memory buffer and display it
        data = io.BytesIO()
        m.save(data, close_file=False)
        self.map_view.setHtml(data.getvalue().decode())