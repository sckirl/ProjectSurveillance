import pymssql
from datetime import datetime
import random

class DatabaseWorker:
    def __init__(self, server="localhost", 
                 port=1433, 
                 user="sa", 
                 password="N0t3431@lv", 
                 database="master"):
        self.conn = pymssql.connect(server=server, port=port, user=user, password=password, database=database)
        self.cursor = self.conn.cursor()

    def createTable(self):
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
        
        if record_id == None:
            record_id = random.getrandbits(100)

        if timestamp is None:
            timestamp = datetime.now()
        self.cursor.execute("""
        INSERT INTO SurveillanceDB (surveillanceID, surveillanceTime, surveillanceImg, latitude, longitude, altitude)
        VALUES (%s, %s, %s, %s, %s, %s)
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
    db.createTable()
    db.insertCoordinates("098", "324.3455", "55.2344", "234.23")
    print(db.fetch_all())
    db.close()