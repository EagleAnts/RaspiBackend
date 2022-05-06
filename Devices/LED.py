from gpiozero import OutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import LED
from time import sleep

factory = PiGPIOFactory(host="192.168.0.120")
led = OutputDevice(5, pin_factory=factory)
