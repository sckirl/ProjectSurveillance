# 👁️ Surveillance System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/) [![PySide6](https://img.shields.io/badge/GUI-PySide6-41cd52?style=for-the-badge&logo=qt&logoColor=white)](https://doc.qt.io/qtforpython/) [![YOLOv8](https://img.shields.io/badge/AI-Ultralytics_YOLO-yellow?style=for-the-badge&logo=ultralytics&logoColor=black)](https://github.com/ultralytics/ultralytics) [![MSSQL](https://img.shields.io/badge/Database-MSSQL-red?style=for-the-badge&logo=microsoft-sql-server&logoColor=white)](https://www.microsoft.com/en-us/sql-server)

**Surveillance System** is a sophisticated desktop application designed for real-time security monitoring. Leveraging the power of computer vision and thermal imaging, it detects human presence, logs incidents to a secure database, and visualizes threats on an interactive map.

---

## 🚀 Key Features

*   **🤖 Real-Time Detection:** Utilizes advanced YOLO-based models to detect humans in video feeds, compatible with both standard and thermal cameras.
*   **🚨 Instant Alerts:** Provides immediate visual feedback and alerts upon detecting potential security threats (e.g., "Human Detected").
*   **💾 Database Integration:** Automatically logs every detection event with high-resolution snapshots, timestamps, and geolocation data into a Microsoft SQL Server.
*   **🗺️ Geospatial Tracking:** Integrates an interactive map (via Folium & OpenMapTiles) to pinpoint the exact location of detection events.
*   **🖥️ Dashboard GUI:** A comprehensive PySide6 interface allowing users to:
    *   View live camera feeds.
    *   Browse and filter historical detection records.
    *   Update or delete incident data.
    *   Visualize data points on a map.

---

## 🛠️ Technologies Used

*   **Language:** [Python 3](https://www.python.org/)
*   **GUI Framework:** [PySide6 (Qt)](https://doc.qt.io/qtforpython/)
*   **Computer Vision:** [OpenCV](https://opencv.org/), [Ultralytics YOLO](https://docs.ultralytics.com/)
*   **Database:** [MSSQL](https://www.microsoft.com/en-us/sql-server) (via `pymssql`)
*   **Mapping:** [Folium](https://python-visualization.github.io/folium/), `openmaptiles`

---

## ⚙️ Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/YourUsername/projectsurveillance.git
    cd projectsurveillance
    ```

2.  **Set up a Virtual Environment (Recommended)**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Setup**
    *   Ensure you have a running MSSQL Server instance.
    *   Execute the `SELECT _ FROM SurveillanceDB.sql` script (or equivalent schema setup) to create the necessary tables.

---

## 🔧 Configuration

Create a `.env` file in the root directory and configure your environment variables:

```env
# Database Configuration
SERVER_LOCATION=your_server_ip
SERVER_PORT=1433
SERVER_USER=your_db_user
SERVER_PASSWORD=your_db_password
DATABASE_NAME=SurveillanceDB

# AI Model Configuration
DETECTION_MODEL=MODELS/HumanDetect.pt  # Path to your YOLO model
DETECTION_TRACKER=bytetrack.yaml       # Tracker configuration
```

---

## 🎮 Usage

Run the main application entry point:

```bash
python main.py
```

### Navigating the Interface:
1.  **Camera Tab:** Select your input source from the dropdown. The system will start detecting and alerting automatically.
2.  **Records Tab:** View a table of all logged incidents. Double-click a row to view details.
3.  **Details & Map Tab:** See the specific snapshot of the intruder and their location on the map. You can update coordinates or delete false positives here.

---

## 📂 Project Structure

```text
D:\projectsurveillance\
├── InterfaceAccess\       # UI forms and assets (.ui files)
├── MODELS\                # Pre-trained YOLO detection models (.pt)
├── CameraAccess.py        # Camera handling and detection logic
├── DatabaseAccess.py      # MSSQL database interactions
├── MapAccess.py           # Map rendering and updating
├── main.py                # Application entry point
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.