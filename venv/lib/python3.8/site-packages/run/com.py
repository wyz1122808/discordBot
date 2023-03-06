# This file is placed in the Public Domain.
# pylint: disable=W0613,W0221,W0201,C0112,C0103,C0114,C0115,C0116,R0902,R0903


class Commands():

    cmds = {}

    @staticmethod
    def add(cmd) -> None:
        Commands.cmds[cmd.__name__] = cmd

    @staticmethod
    def get(cmd):
        return Commands.cmds.get(cmd)

    @staticmethod
    def remove(cmd: str) -> None:
        del Commands.cmds[cmd]


def dispatch(evt) -> None:
    evt.parse()
    func = Commands.get(evt.cmd)
    if func:
        func(evt)
        evt.show()
    evt.ready()
