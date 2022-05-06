import sqlite3
import sys

port = sys.argv[-1]


class SQLiteDB:
    def __init__(self) -> None:
        self.conn, self.cur = self.connectDB()

    def connectDB(self):
        try:

            conn = sqlite3.connect(f"pi:{port}.db")
            print("SQL Lite Connected")
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute('''
            CREATE TABLE IF NOT EXISTS rpiDetails(piID text,networkID text,piName text,user_email text,rpiUsername text,rpiPassword text,token text,serverAddress text);
                ''')
            conn.commit()
            # DROP TABLE rpiDetails

            cur.execute(
                '''CREATE TABLE IF NOT EXISTS users(username text, email text) ;''')
            # Save (commit the changes)
            conn.commit()
            # cur.execute(
            #     '''CREATE TABLE IF NOT EXISTS device(device_id TEXT PRIMARY KEY, name TEXT NOT NULL, device_type TEXT NOT NULL,gpio INTEGER NOT NULL UNIQUE, area TEXT NOT NULL, status INTEGER NOT NULL, FOREIGN KEY (device_type) REFERENCES device_type (type) ;''')
            # # Save (commit the changes)
            # conn.commit()
            # cur.execute(
            #     '''CREATE TABLE IF NOT EXISTS device_type(type TEXT PRIMARY KEY, description TEXT NOT NULL, icon BLOB ) ;''')
            # # Save (commit the changes)
            # conn.commit()
            cur.execute(
                '''CREATE TABLE IF NOT EXISTS blockchain(piID text,blockchain json)''')
            conn.commit()

            return conn, cur
        except:
            print("Error Connecting to Database")

    @staticmethod
    def getAllRows(rowObject):
        if isinstance(rowObject, list):
            for r in rowObject:
                print("(", end=" ")
                for x in r:
                    print(x, end=", ")
                print(" )")

            print("\n")
        else:
            print("(", end=" ")
            for x in rowObject:
                print(x, end=", ")
            print(" )")
            print("\n")

    async def saveToRpiDetails(self, data):
        print("Saving Details in RpiDetails Table... : ", data)
        self.cur.execute(
            "INSERT INTO rpiDetails values(:piID,:networkID,:piName,:email,:rpiusername,:rpipassword,:token,:serverAddress)", data)
        self.conn.commit()

    # async def insertDevice(self, data):
    #     print("Inserting Device Details to device Table... : ", data)
    #     self.cur.execute(
    #         "INSERT INTO device values(:device_id,:name,:device_type,:gpio, :area,:status)", data,)
    #     self.conn.commit()

    # async def insertDeviceType(self, data):
    #     print("Inserting Device Type Details to device_type Table... : ", data)
    #     self.cur.execute(
    #         "INSERT INTO device_type values(:type,:description,:icon)", data,)
    #     self.conn.commit()

    # async def checkIfDevicePresentOnGpio(self, data):
    #     print("Check if a device already exist at a gpio... : ", data)
    #     return self.cur.execute("Select device_id from device WHERE gpio=:gpio", data).fetchone()

    # async def getAllDevice(self):
    #     print("Getting All Device Details in device Table... ")
    #     return self.cur.execute(
    #         "SELECT device.device_id,device.name,device.device_type, device_type.description,device.gpio, device.area,device.status,device.icon FROM device JOIN device_type ON device.device_type = device_type.type")

    # async def updateDeviceStatus(self, data):
    #     print("Updating Device Status in device Table... : ", data)
    #     self.cur.execute(
    #         "UPDATE device SET status=:status WHERE device_id=:device_id", data,)
    #     self.conn.commit()

    async def saveBlockchainDetails(self, data):
        print("Saving Details in Blockchain Table.... :", data)
        self.cur.execute(
            "INSERT INTO blockchain values(:piID,:blockchain)", data
        )
        self.conn.commit()

    async def getRpiDetails(self):
        print("Getting Rpi Details...")
        return self.cur.execute("Select * from rpiDetails").fetchone()

    async def getPIID(self):
        print("Getting PiID..")
        return (self.cur.execute("Select piID from rpiDetails").fetchone())["piID"]

    async def getBlockchainDetails(self):
        print("Getting Blockchain Details")
        return self.cur.execute("Select * from blockchain ")


db = SQLiteDB()
