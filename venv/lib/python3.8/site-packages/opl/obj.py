# This file is placed in the Public Domain.
# pylint: disable=W0613,W0221,C0112,C0103,C0114,C0115,C0116,R0903,W0622


"""Big Object is a load/saveable python object

This module contains a big Object class that provides a clean, no methods,
namespace for json data to be read into. This is necessary so that methods
don't get overwritten by __dict__ updating and, without methods defined on
the object, is easily being updated from a on disk stored json (dict).

basic usage is this::

 >>> import opl
 >>> o = opl.Object()
 >>> o.key = "value"
 >>> o.key
 'value'

Some hidden methods are provided, methods are factored out into functions
like get, items, keys, register, set, update and values.

load/save from/to disk::

 >>> import opl
 >>> o = opl.Object()
 >>> o.key = "value"
 >>> p = opl.save(o)
 >>> oo = opl.Object()
 >>> opl.load(oo, p)
 >>> oo.key
 'value'

Big Objects can be searched with database functions and uses read-only files
to improve persistence and a type in filename for reconstruction::

 'opl.obj.Object/2021-08-31/15:31:05.717063'

 >>> import opl
 >>> o = opl.Object()
 >>> opl.save(o)  # doctest: +ELLIPSIS
 'opl.obj.Object/...'

Great for giving objects peristence by having their state stored in files.

"""


import datetime
import os
import types


from opl.cls import Class


def __dir__():
    return (
            'Class',
            'Default',
            'Object',
            'Wd',
            'delete',
            'edit',
            'format',
            'get',
            'items',
            'jsn',
            'keys',
            'name',
            'otype',
            'register',
            'save',
            'types',
            'update',
            'values'
           )


class Object:

    """Big Objects load/save themselves to/from disk.

       It has no methods, it's __dict__ is clean on start (clean namespace).
       Method are implemented as functions with the object as the first
       argument, a trick to mimic object method calls.

       >>> import opl
       >>> o = opl.Object()
       >>> o.test = "try"
       >>> opl.format(o)
       'test=try'

       Some hidden methods are provided, methods are factored out into functions
       like get, items, keys, register, set, update and values.

    """

    __slots__ = ('__dict__','__stp__')

    def __init__(self, *args, **kwargs):
        object.__init__(self)
        self.__stp__ = os.path.join(
            otype(self),
            os.sep.join(str(datetime.datetime.now()).split()),
        )
        if args:
            update(self, args[0])

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self. __dict__)


Class.add(Object)


def delete(obj, key):
    "Delete `key` attribute."
    delattr(obj, key)


def edit(obj, setter):
    "Changes attributes based on dict values."
    for key, value in items(setter):
        register(obj, key, value)


def format(obj, args="", skip="", plain=False):
    "Format an object to a printable string."
    res = []
    keyz = []
    if "," in args:
        keyz = args.split(",")
    if not keyz:
        keyz = keys(obj)
    for key in keyz:
        if key.startswith("_"):
            continue
        if skip:
            skips = skip.split(",")
            if key in skips:
                continue
        value = getattr(obj, key, None)
        if not value:
            continue
        if " object at " in str(value):
            continue
        txt = ""
        if plain:
            txt = str(value)
        elif isinstance(value, str) and len(value.split()) >= 2:
            txt = '%s="%s"' % (key, value)
        else:
            txt = '%s=%s' % (key, value)
        res.append(txt)
    txt = " ".join(res)
    return txt.rstrip()


def get(obj, key, default=None):
    "Return attribute `key`."
    return obj.__dict__.get(key, default)


def name(obj):
    "Return full qualified name."
    typ = type(obj)
    if isinstance(typ, types.ModuleType):
        return obj.__name__
    if "__self__" in dir(obj):
        return "%s.%s" % (obj.__self__.__class__.__name__, obj.__name__)
    if "__class__" in dir(obj) and "__name__" in dir(obj):
        return "%s.%s" % (obj.__class__.__name__, obj.__name__)
    if "__class__" in dir(obj):
        return obj.__class__.__name__
    if "__name__" in dir(obj):
        return obj.__name__
    return None


def items(obj):
    "Return all assigned attributes."
    if isinstance(obj, type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj):
    "Return all attribute names."
    return obj.__dict__.keys()


def otype(obj):
    "Return type of the object."
    return str(type(obj)).split()[-1][1:-2]


def register(obj, key, value):
    "Register an attribute."
    setattr(obj, key, value)


def update(obj, data):
    "Update this object with another object/dict."
    if isinstance(data, type({})):
        obj.__dict__.update(data)
    else:
        obj.__dict__.update(vars(data))


def values(obj):
    "Return the values of assigned attributes."
    return obj.__dict__.values()
