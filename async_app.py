import socketio
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from signal import pause

factory1 = PiGPIOFactory(host='192.168.0.112')
blueLed = LED(4, pin_factory=factory1)

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = socketio.ASGIApp(sio, static_files={
    '/': './public/'
})


@sio.event
async def connect(sid, enviro):
    print('connected with id ', sid)


@sio.event
async def disconnect(sid):
    print('disconnected', sid)


@sio.event
async def deviceOn(sid, data):
    if data['type'] == "Lights":
        if data['active']:
            print("Turning on led ....")
            blueLed.on()
        else:
            print("Turing off led ...")
            blueLed.off()
