import pyodbc
from datetime import datetime

class SurveillanceDB:
    def __init__(self, server="localhost,1433", 
                 database="master", 
                 username="sa", 
                 password="N0t3431@lv"):
        
        self.conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={server};DATABASE={database};"
            f"UID={username};PWD={password};"
            f"Encrypt=yes; TrustServerCertificate=yes;"
        )
        self.cursor = self.conn.cursor()
        self.create_table()

    def insert_coordinates(self, 
                           record_id, 
                           latitude, 
                           longitude, 
                           altitude, 
                           img=None, 
                           timestamp=datetime.now()):
        """Insert a record with coordinates (and optional image)."""
        self.cursor.execute("""
        INSERT INTO Surveillance (surveillanceID, surveillanceTime, surveillanceImg, latitude, longitude, altitude)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (record_id, timestamp, img, latitude, longitude, altitude))
        self.conn.commit()

    def fetch_all(self):
        self.cursor.execute("SELECT surveillanceID, surveillanceTime, latitude, longitude, altitude FROM Surveillance")
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    db = SurveillanceDB()

    # Insert example record with just coordinates
    db.insert_coordinates("what", "123.3455", "3123.2344", "1233.23")

    # Fetch all records
    for row in db.fetch_all():
        print(row)

    db.close()