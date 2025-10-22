import io
import os
import re
import sqlite3
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import folium
from PySide6.QtGui import QDesktopServices
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView


def _detect_mbtiles_format(mbtiles_path: str):
    """Read metadata table and return 'jpg' or 'png' depending on format recorded in metadata."""
    try:
        conn = sqlite3.connect(mbtiles_path)
        cur = conn.cursor()
        cur.execute("SELECT value FROM metadata WHERE name='format'")
        row = cur.fetchone()
        conn.close()
        if row and row[0]:
            fmt = row[0].lower()
            if 'jpg' in fmt or 'jpeg' in fmt:
                return 'jpg'
            if 'png' in fmt:
                return 'png'
    except Exception:
        pass
    return 'png'


class _MBTilesHTTPRequestHandler(BaseHTTPRequestHandler):
    # path: /tiles/{z}/{x}/{y}.{ext}
    URL_RE = re.compile(r"^/tiles/(\d+)/(\d+)/(\d+)\.(png|jpg)$")

    def do_GET(self):
        m = self.URL_RE.match(self.path)
        if not m:
            self.send_response(404)
            self.end_headers()
            return

        z, x, y, ext = m.groups()
        z = int(z); x = int(x); y = int(y)
        # Convert from XYZ (Leaflet) to TMS row used by MBTiles
        tms_y = (2 ** z - 1) - y

        try:
            conn = sqlite3.connect(self.server.mbtiles_path)
            cur = conn.cursor()
            cur.execute("SELECT tile_data FROM tiles WHERE zoom_level=? AND tile_column=? AND tile_row=?",
                        (z, x, tms_y))
            row = cur.fetchone()
            conn.close()
            if not row or not row[0]:
                self.send_response(404)
                self.end_headers()
                return

            blob = row[0]
            self.send_response(200)
            ctype = 'image/jpeg' if ext == 'jpg' else 'image/png'
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(len(blob)))
            self.end_headers()
            self.wfile.write(blob)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            try:
                self.wfile.write(str(e).encode())
            except Exception:
                pass


class _MBTilesServer:
    def __init__(self, mbtiles_path: str, port: int = 5001):
        self.mbtiles_path = mbtiles_path
        self.port = port
        self.httpd = None
        self.thread = None
        self.is_running = False

    def start(self):
        if not os.path.exists(self.mbtiles_path):
            raise FileNotFoundError(self.mbtiles_path)

        handler = _MBTilesHTTPRequestHandler
        # attach path to server instance via lambda closure
        def _handler(*args, **kwargs):
            handler(*args, **kwargs)

        # ThreadingHTTPServer will set handler.server later; we set attribute after creation
        self.httpd = ThreadingHTTPServer(('127.0.0.1', self.port), handler)
        self.httpd.mbtiles_path = self.mbtiles_path
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.is_running = True

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
        self.is_running = False

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
        
        # MBTiles support: look for an MBTiles file next to this module named 'offline.mbtiles'
        self._mbtiles_path = os.path.join(os.path.dirname(__file__), "offline.mbtiles")
        self._mbtiles_server = None
        self._mbtiles_format = None
        if os.path.exists(self._mbtiles_path):
            try:
                self._mbtiles_format = _detect_mbtiles_format(self._mbtiles_path)
                port = 5001
                self._mbtiles_server = _MBTilesServer(self._mbtiles_path, port)
                self._mbtiles_server.start()
                print(f"MBTiles server started on port {port} (format={self._mbtiles_format})")
            except Exception as e:
                print(f"Failed to start MBTiles server: {e}")

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

        # Create the map. If we have an mbtiles server running, use it as a TileLayer.
        if self._mbtiles_server and self._mbtiles_server.is_running:
            # Use tiles=None to avoid default tiles
            m = folium.Map(location=coords, zoom_start=13, tiles=None)
            ext = self._mbtiles_format or 'png'
            tiles_url = f"http://127.0.0.1:{self._mbtiles_server.port}/tiles/{{z}}/{{x}}/{{y}}.{ext}"
            folium.TileLayer(
                tiles=tiles_url,
                attr="Offline MBTiles",
                name="Offline",
                overlay=False,
                control=True
            ).add_to(m)
        else:
            # Fallback to default tiles
            m = folium.Map(location=coords, zoom_start=13)

        try: 
            # Create the Google Maps URL and popup HTML
            gmaps_url = f"https://www.google.com/maps/search/?api=1&query={coords[0]},{coords[1]}"
            popup_html = f'<a href="{gmaps_url}" target="_blank">Open in Google Maps</a>'

            # Add a marker to the map
            folium.Marker(
                location=coords,
                popup=popup_html,
                tooltip="Click fo sr options",
            ).add_to(m)
        except Exception as e:
            print(e)

        # Save map data to an in-memory buffer and display it
        data = io.BytesIO()
        m.save(data, close_file=False)
        self.map_view.setHtml(data.getvalue().decode())