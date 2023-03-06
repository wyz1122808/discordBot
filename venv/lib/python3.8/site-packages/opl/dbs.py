# This file is placed in the Public Domain.
# pylint: disable=E1101,W0613,W0221,C0112,C0103,C0114,C0115,C0116,R0903


"database"


import _thread


from opl.obj import Object, get, items, otype, update
from opl.cls import Class
from opl.jsn import hook
from opl.sel import Selector
from opl.wdr import Wd
from opl.utl import fns, fntime


dblock = _thread.allocate_lock()


def __dir__():
    return (
            "Db",
            "find",
            "last",
            "search"
           )

def locked(lock):

    def lockeddec(func, *args, **kwargs):

        def lockedfunc(*args, **kwargs):
            lock.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                lock.release()
            return res

        lockeddec.__wrapped__ = func
        lockeddec.__doc__ = func.__doc__
        return lockedfunc

    return lockeddec


class Db():

    @staticmethod
    def all(otp, timed=None):
        result = []
        for fnm in fns(Wd.getpath(otp), timed):
            obj = hook(fnm)
            if "__deleted__" in obj and obj.__deleted__:
                continue
            result.append((fnm, obj))
        if not result:
            return []
        return result

    @staticmethod
    def find(otp, selector=None, index=None, timed=None):
        if selector is None:
            selector = {}
        _nr = -1
        result = []
        for fnm in fns(Wd.getpath(otp), timed):
            obj = hook(fnm)
            if selector and not search(obj, selector):
                continue
            if "__deleted__" in obj and obj.__deleted__:
                continue
            _nr += 1
            if index is not None and _nr != index:
                continue
            result.append((fnm, obj))
        return result

    @staticmethod
    def last(otp):
        fnm = fns(Wd.getpath(otp))
        if fnm:
            fnn = fnm[-1]
            return (fnn, hook(fnn))
        return (None, None)

    @staticmethod
    def match(otp, selector=None, index=None, timed=None):
        res = sorted(
                     Db.find(otp, selector, index, timed), key=lambda x: fntime(x[0]))
        if res:
            return res[-1]
        return (None, None)


def find(name, selector=None, index=None, timed=None):
    names = Class.full(name)
    if not names:
        names = Wd.types(name)
    db = Db()
    result = []
    for nme in names:
        for fnm, obj in db.find(nme, selector, index, timed):
            result.append((fnm, obj))
    return result


def last(obj):
    db = Db()
    _path, _obj = db.last(otype(obj))
    if _obj:
        update(obj, _obj)


def search(obj, selector):
    res = False
    select = Selector(selector)
    for key, value in items(select):
        val = get(obj, key)
        if str(value) in str(val):
            res = True
            break
    return res
