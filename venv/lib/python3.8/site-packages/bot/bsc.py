# This file is placed in the Public Domain.
# pylint: disable=C0114,C0115,C0116


import time


from opl.utl import elapsed
from run import Commands, starttime


def cmd(event):
    event.reply(",".join(sorted(Commands.cmds)))


def upt(event):
    event.reply(elapsed(time.time()-starttime))
