# This file is placed in the Public Domain.
# pylint: disable=W0613,W0221,W0201,C0112,C0103,C0114,C0115,C0116,R0902,R0903


"list of Objects. Object should provides sa say(channel, txt)."


from opl import Object


class Bus():

    objs = []

    @staticmethod
    def add(obj: Object) -> None:
        if repr(obj) not in [repr(x) for x in Bus.objs]:
            Bus.objs.append(obj)

    @staticmethod
    def announce(txt: str) -> None:
        for obj in Bus.objs:
            if obj and "announce" in dir(obj):
                obj.announce(txt)

    @staticmethod
    def byorig(orig: str) -> Object:
        res = None
        for obj in Bus.objs:
            if repr(obj) == orig:
                res = obj
                break
        return res

    @staticmethod
    def say(orig: str, channel: str, txt: str) -> None:
        obj = Bus.byorig(orig)
        if obj and "say" in dir(obj):
            obj.say(channel, txt)
