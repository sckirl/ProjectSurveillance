import pymssql
from datetime import datetime
import uuid

class DatabaseWorker:
    def __init__(self, server="localhost", 
                 port=1433, 
                 user="sa", 
                 password="N0t3431@lv", 
                 database="master"):
        
        self.is_connected = False
        try: 
            self.conn = pymssql.connect(server=server, port=port, user=user, password=password, database=database)
            self.cursor = self.conn.cursor()
            self.is_connected = True
            print("Database connection successful.")
        except Exception as e:
            print(f"Connection can't be established: {e}")

    def generate_next_id(self):
        """Generates the next ID in sequence, preventing race conditions."""
        if not self.is_connected: return None
        
        today_str = datetime.now().strftime('%d%m%Y')
        
        try:
            # --- CHANGE 1: Add locking hints to make the read atomic ---
            # This tells SQL Server to lock the row it's reading until the transaction is complete.
            self.cursor.execute("""
            SELECT TOP 1 surveillanceID 
            FROM SurveillanceDB WITH (UPDLOCK, HOLDLOCK)
            WHERE surveillanceID LIKE %s
            ORDER BY surveillanceID DESC
            """, (today_str + '%',))
            
            last_id = self.cursor.fetchone()
            
            if last_id:
                last_sequence = int(last_id[0][8:])
                new_sequence = last_sequence + 1
            else:
                new_sequence = 1
                
            new_id = f"{today_str}{new_sequence:04d}"
            return new_id
            
        except Exception as e:
            print(f"Error generating new ID: {e}")
            self.conn.rollback() # Rollback the transaction on error
            return None
        
    def createTable(self):
        if not self.is_connected: return
        self.cursor.execute("""
        IF OBJECT_ID('SurveillanceDB', 'U') IS NULL
        CREATE TABLE SurveillanceDB (
            surveillanceID CHAR(36) PRIMARY KEY,
            surveillanceTime DATETIME,
            surveillanceImg VARBINARY(MAX),
            latitude VARCHAR(20),
            longitude VARCHAR(20),
            altitude VARCHAR(20)
        )
        """)
        self.conn.commit()

    def insertCoordinates(self, 
                          latitude, 
                          longitude, 
                          altitude, 
                          record_id=None,
                          img=None, 
                          timestamp=None):
        
        if not self.is_connected: return
        record_id = self.generate_next_id()
        if not record_id:
            print("Failed to generate a new record ID. Aborting insert.")
            return

        if timestamp is None:
            timestamp = datetime.now()

        self.cursor.execute("""
        INSERT INTO SurveillanceDB (surveillanceID, surveillanceTime, surveillanceImg, latitude, longitude, altitude)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (record_id, timestamp, img, latitude, longitude, altitude))
        self.conn.commit()

    def update_coordinates(self, record_id, latitude, longitude, altitude):
        if not self.is_connected: return False
        try:
            self.cursor.execute("""
            UPDATE SurveillanceDB
            SET latitude = %s, longitude = %s, altitude = %s
            WHERE surveillanceID = %s
            """, (latitude, longitude, altitude, record_id))
            self.conn.commit()
            print(f"Successfully updated coordinates for ID: {record_id}")
            return True
        except Exception as e:
            print(f"Error updating coordinates for ID {record_id}: {e}")
            return False

    def fetch_all_data(self):
        if not self.is_connected: return []
        try:
            self.cursor.execute("""
            SELECT surveillanceID, surveillanceTime, surveillanceImg, latitude, longitude, altitude 
            FROM SurveillanceDB 
            ORDER BY surveillanceTime DESC
            """)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching all data: {e}")
            return []

    def fetch_record_by_id(self, record_id):
        """Fetches a single, complete record from the database by its ID."""
        if not self.is_connected: return None
        try:
            self.cursor.execute("""
            SELECT surveillanceID, surveillanceTime, surveillanceImg, latitude, longitude, altitude 
            FROM SurveillanceDB WHERE surveillanceID = %s
            """, (record_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching record by ID {record_id}: {e}")
            return None

    def close(self):
        if not self.is_connected: return
        self.cursor.close()
        self.conn.close()