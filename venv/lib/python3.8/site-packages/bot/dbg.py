# This file is placed in the Public Domain.
# pylint: disable=E1101


"debug"


import threading
import time


from opl import Object, get, name, update
from opl.utl import elapsed

from run import Bus, starttime


def __dir__():
    return (
            "flt",
            "thr"
           )


def flt(event):
    "show bots registered on the bus."
    try:
        index = int(event.args[0])
        event.reply(Bus.objs[index])
        return
    except (KeyError, TypeError, IndexError, ValueError):
        pass
    event.reply(" | ".join([name(o) for o in Bus.objs]))


def thr(event):
    "show running threads."
    result = []
    for thread in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thread).startswith("<_"):
            continue
        obj = Object()
        update(obj, vars(thread))
        if get(obj, "sleep", None):
            uptime = obj.sleep - int(time.time() - obj.state.latest)
        else:
            uptime = int(time.time() - starttime)
        result.append((uptime, thread.getName()))
    res = []
    for uptime, txt in sorted(result, key=lambda x: x[0]):
        res.append("%s/%s" % (txt, elapsed(uptime)))
    if res:
        event.reply(" ".join(res))
    else:
        event.reply("no threads running")
