import sys
import io
import folium

# Import necessary PyQt6 components
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView

<<<<<<< HEAD
=======
# --- Step 1: Create the PyQt Application Window ---
>>>>>>> master
class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive Map in PyQt")
        self.setGeometry(100, 100, 900, 700)

        # --- Step 2: Create the Folium Map ---
        # Coordinates for Jakarta
        jakarta_coords = [-6.2088, 106.8456]
        m = folium.Map(location=jakarta_coords, zoom_start=12)

        # Add a marker for Monas
        folium.Marker(
            location=[-6.1754, 106.8272],
            popup="Monas",
            tooltip="Click Here!"
        ).add_to(m)

        # --- Step 3: Save Map to memory and Display in PyQt ---
        # Save map data to an in-memory buffer
        data = io.BytesIO()
        m.save(data, close_file=False)

        # Create a QWebEngineView widget (the mini-browser)
        browser = QWebEngineView()
        # Set the HTML from the in-memory buffer
        browser.setHtml(data.getvalue().decode())

        # Set the browser widget as the central widget of the window
        self.setCentralWidget(browser)

# --- Run the Application ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec())