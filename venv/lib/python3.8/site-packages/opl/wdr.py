# This file is placed in the Public Domain.
# pylint: disable=C0112,C0103,C0114,C0115,C0116


"working directory"


import os


class Wd:

    workdir = ".opl"

    @staticmethod
    def get():
        return Wd.workdir

    @staticmethod
    def getpath(path):
        return os.path.join(Wd.workdir, "store", path)

    @staticmethod
    def set(val):
        Wd.workdir = val

    @staticmethod
    def storedir():
        return os.path.join(Wd.workdir, "store", '')

    @staticmethod
    def types(name=None):
        sdr = Wd.storedir()
        res = []
        for fnm in os.listdir(sdr):
            if name and name.lower() not in fnm.split(".")[-1].lower():
                continue
            if fnm not in res:
                res.append(fnm)
        return res
