<!-- Copilot / AI agent instructions for ProjectSurveillance -->
# ProjectSurveillance — Copilot instructions

These notes help an AI assistant be productive in this repository. Keep responses short, concrete, and reference files below when suggesting edits.

- Big picture: a PySide6 desktop app (UI built with Qt Designer .ui) that captures video, runs a YOLO detection+tracking model, performs small OCR on fixed ROIs, and stores detection snapshots and coordinates into a SQL Server database.

- Key entry points/files:
  - `main.py` — application wiring: loads the `.ui` (path from env `INTERFACE`), creates `DatabaseWorker`, `CameraWorker`, and `MapWorker`, and hooks UI signals.
  - `CameraAccess.py` — `CameraWorker` (QObject) runs in a QThread, uses `ultralytics.YOLO.track`, emits signals: `frameUpdated(QPixmap)`, `detectionOccurred(bytes,message,lat,lon)`, `visionStatus(str)`, `finished()`.
  - `DatabaseAccess.py` — `DatabaseWorker` wraps `pymssql`; table name `SurveillanceDB` and columns: `surveillanceID, surveillanceTime, surveillanceImg, latitude, longitude, altitude`. Use its helper methods: `insertCoordinates`, `fetch_all_data`, `fetch_record_by_id`, `update_coordinates`, `delete_by_id`.
  - `MapAccess.py` — `MapWorker` uses `folium` and displays HTML in a `QWebEngineView`. It uses `WebEnginePage` to open external links.

- Important runtime conventions:
  - The app depends on environment variables (loaded by `dotenv` in `main.py`): `INTERFACE`, `SERVER_LOCATION`, `SERVER_PORT`, `SERVER_USER`, `SERVER_PASSWORD`, `DATABASE_NAME`, `DETECTION_MODEL`, `DETECTION_TRACKER`.
  - The UI is a Qt `.ui` file referenced by `INTERFACE`. Changes to UI ids must match lookups in `main.py` (e.g., `CameraComboBox`, `videoDisplayWidget`, `MapWebView`).
  - `CameraWorker.run()` is long-lived; it must be stopped with `camera_worker.stop()` and the thread joined (`quit()`, `wait()`) before app exit.

- Patterns & conventions to follow when editing code:
  - Threading: long-running work goes into `QObject` workers moved to `QThread`. Connect signals instead of calling UI methods directly from worker threads.
  - Signals: use the existing signal names and signatures exactly (e.g., `detectionOccurred(bytes, str, str, str)`) when emitting or connecting handlers.
  - Database IDs: `DatabaseWorker.generate_next_id()` produces IDs based on date + sequence; prefer using `insertCoordinates()` rather than manual inserts to keep ID logic consistent.
  - Image payloads: detection images are JPEG-encoded bytes (from `cv2.imencode`) and decoded using `np.frombuffer(...); cv2.imdecode(...)` in `main.py`.
  - OCR regions: `CameraWorker` performs OCR on two hard-coded ROIs: `roi_latitude = (20, 390, 200, 30)` and `roi_longitude = (415, 390, 200, 30)`. If changing UI/camera framing, update these ROIs accordingly.

- External integrations and dependencies:
  - Model: `ultralytics.YOLO` (specified model path via `DETECTION_MODEL`). Tracking uses the `tracker` parameter (default `botsort.yaml`).
  - DB: Microsoft SQL Server via `pymssql` (credentials from env). The schema expected by the code is in `DatabaseAccess.py` (see the `createTable` method).
  - UI: PySide6 (Qt) and PySide6 WebEngine for map display. Folium is used to generate tile HTML.

- Developer workflow & quick commands (macOS, zsh):
  - Create and activate a venv, install requirements:
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
  - Run the app (ensure `.env` has the required env vars, and `INTERFACE` points to the `.ui` file):
    python main.py
  - Tests: no test suite present; run manual UI flows. When changing workers, manually verify thread stop/cleanup on exit.

- Files to inspect when changing behavior:
  - UI lookups and names: `main.py` (search for `findChild(...)`) — changing widget names here must match the `.ui` file.
  - Detection and OCR: `CameraAccess.py` (check `PROCESS_INTERVAL`, `perform_ocr`, and `detection_buffer` aggregation logic).
  - DB interactions: `DatabaseAccess.py` (transaction handling, `commit()`/`rollback()` patterns; `generate_next_id()` design).
  - Map rendering: `MapAccess.py` (folium map creation and `setHtml()` usage).

- Small, actionable heuristics for code suggestions:
  - When modifying image processing, prefer returning JPEG bytes for storage and use existing decode paths in `main.py` to render previews.
  - Preserve signal signatures and worker thread lifecycle when adding features.
  - If adding new environment configuration, add a default fallback in code or document the new env key in README/.env.
  - Avoid changing database schema without updating `DatabaseWorker.createTable()` and all call sites.

- Example references (copy/paste snippets):
  - Emitting detection: `self.detectionOccurred.emit(image_bytes, detection_message, lat_text, lon_text)` (see `CameraAccess.py`).
  - Map call: `self.mapWorker.update_map(latitude, longitude)` (see `main.py#getChosenID`).

If any part is unclear or you want additional details (e.g., the UI `.ui` file path, how to run with a camera index vs. video file, or adding unit tests), tell me which area to expand. Update request: do you want examples of safe refactors (type hints, tests) included?
