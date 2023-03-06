# This file is placed in the Public Domain.
# pylint: disable=W0613,W0221,W0201,C0112,C0103,C0114,C0115,C0116,R0902,R0903


"handler"


import queue
import threading
import time


from opl import Object


from run.bus import Bus
from run.cbs import Callbacks
from run.evt import Event
from run.thr import launch


class Handler(Object):

    def __init__(self):
        Object.__init__(self)
        self.cache = Object()
        self.queue = queue.Queue()
        self.stopped = threading.Event()
        Bus.add(self)

    @staticmethod
    def forever() -> None:
        while 1:
            time.sleep(1.0)

    @staticmethod
    def handle(event) -> None:
        Callbacks.dispatch(event)

    def loop(self) -> None:
        while not self.stopped.isSet():
            self.handle(self.poll())

    def poll(self) -> Event:
        return self.queue.get()

    def put(self, event: Event) -> None:
        self.queue.put_nowait(event)

    @staticmethod
    def register(typ, cbs) -> None:
        Callbacks.add(typ, cbs)

    def restart(self) -> None:
        self.stop()
        self.start()

    def start(self) -> None:
        self.stopped.clear()
        launch(self.loop)

    def stop(self) -> None:
        self.stopped.set()
