import asyncio
import signal
import functools
from Helpers.socketIoServer import app as SocketIoApp

app = SocketIoApp


# async def shutdown(sig, loop):
#     print(f'Caught {sig.name}')
#     tasks = [task for task in asyncio.all_tasks(
#     ) if task is not asyncio.current_task()]
#     list(map(lambda task: task.cancel(), tasks))
#     results = await asyncio.gather(*tasks, return_exceptions=True)
#     print(f"Finished Awaiting Cancelled Tasks, results : {results}")
#     loop.close()


# loop = asyncio.get_running_loop()
# loop.add_signal_handler(signal.SIGINT, functools.partial(
#     asyncio.ensure_future, shutdown(signal.SIGINT, loop)))


# checkRegisterationTask = asyncio.get_event_loop().create_task(main())
# checkRegisterationTask.add_done_callback(lambda t: print(
#     f'Task done with result={t.result()}  << return val of main()'))

# from gpiozero import LED
# from gpiozero.pins.pigpio import PiGPIOFactory
# from time import sleep
# from signal import pause
