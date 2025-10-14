import pymssql
from datetime import datetime
import uuid

class DatabaseWorker:
    def __init__(self, server, 
                 port, 
                 user, 
                 password, 
                 database):
        
        self.is_connected = False
        try: 
            self.conn = pymssql.connect(server=server, port=port, user=user, password=password, database=database)
            self.cursor = self.conn.cursor()
            self.is_connected = True
            print("Database connection successful.")
            
        except Exception as e:
            print(f"Connection can't be established: {e}")
            print(f"Check if the database is running")
            self.is_connected = False

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

    def get_last_id(self):
        # --- CHANGE 1: Add locking hints to make the read atomic ---
        # This tells SQL Server to lock the row it's reading until the transaction is complete.
        self.cursor.execute("""
            SELECT TOP 1 surveillanceID 
            FROM SurveillanceDB WITH (UPDLOCK, HOLDLOCK)
            ORDER BY surveillanceID DESC
        """)
        
        last_id = self.cursor.fetchone()

        return last_id
        
    def generate_next_id(self):
        """Generates the next ID in sequence, preventing race conditions."""
        if not self.is_connected: return None
        
        today_str = datetime.now().strftime('%d%m%Y')
        
        try:
            last_id = self.get_last_id()
            
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
        

    def delete_by_id(self, record_id):
        if not self.is_connected: return False # Return False if not connected

        try:
            self.cursor.execute("""
            DELETE FROM SurveillanceDB WHERE surveillanceID = %s
            """, (record_id,)) # Using a tuple (record_id,) is safer

            self.conn.commit() # <<< 1. THE CRITICAL FIX: Save the change to the database.

            print(f"Successfully deleted record ID: {record_id}")
            return True # <<< 2. RETURN TRUE to indicate success.

        except Exception as e:
            print(f"Failed to delete id: {record_id} with error: {e}")
            self.conn.rollback() # It's good practice to roll back on error
            return False # <<< 3. RETURN FALSE to indicate failure.

    def close(self):
        if not self.is_connected: return
        self.cursor.close()
        self.conn.close()