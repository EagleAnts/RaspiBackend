import socketio

sio = socketio.AsyncClient(
    reconnection=True, reconnection_delay=1)


# cur = db.cur
# cur.execute("Select name from sqlite_master where type='table';")
# SQLiteDB.getAllRows(cur.fetchall())
# cur.execute("PRAGMA table_info('rpiDetails')")
# SQLiteDB.getAllRows(cur.fetchall())
# cur.execute("Select * from rpiDetails")
# SQLiteDB.getAllRows(cur.fetchall())

# @sio.event(namespace="/raspberrypi")
# async def connect():
#     print("Connected to Server Successfully")
# @sio.event(namespace="/raspberrypi")
# async def disconnect():
#     print("Disconnected with Server")
# @sio.event(namespace="/raspberrypi")
# async def connect_error():
#     print("Connection Error")

# @sio.on("*", namespace="/raspberrypi")
# async def catch_all(event, args):
#     print(event, args)

# async def connectToBlockchain(ENDPOINT="http://192.168.0.118:5000"):
#     if "/blockchain" not in sio.connection_namespaces:
#         await sio.connect(ENDPOINT, namespaces="/blockchain")

# register mongodb, blockchain network mongodb, mongo newn,
