# This file is placed in the Public Domain.
# pylint: disable=W0613,W0221,W0201,C0112,C0103,C0114,C0115,C0116,R0902,R0903


import threading


from opl import Default, Object, update

from run.bus import Bus
from run.prs import parse


class Event(Default):

    def __init__(self):
        Default.__init__(self)
        self._ready = threading.Event()
        self._result = []
        self.orig = repr(self)
        self.type = "event"

    def bot(self) -> Object:
        return Bus.byorig(self.orig)

    def parse(self) -> None:
        if self.txt:
            update(self, parse(self.txt))

    def ready(self) -> None:
        self._ready.set()

    def reply(self, txt: str) -> None:
        self._result.append(txt)

    def show(self) -> None:
        for txt in self._result:
            Bus.say(self.orig, self.channel, txt)

    def wait(self) -> list:
        self._ready.wait()
        return self._result


def docmd(clt, txt) -> Event:
    cmd = Event()
    cmd.channel = ""
    cmd.orig = repr(clt)
    cmd.txt = txt
    clt.handle(cmd)
    cmd.wait()
    return cmd
