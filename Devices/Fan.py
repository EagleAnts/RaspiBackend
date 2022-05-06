from gpiozero import OutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep


pin_factory = PiGPIOFactory(host="192.168.0.120")
Fan = OutputDevice(6, active_high=False, pin_factory=pin_factory)
