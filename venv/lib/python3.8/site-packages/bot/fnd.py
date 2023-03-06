# This file is placed in the Public Domain.
# pylint: disable=R0903,C0103,C0114,C0115,C0116,W0622


import time


from opl import Wd, elapsed, find, format, fntime, keys


def fnd(event):
    if not event.args:
        res = ",".join(sorted([x.split(".")[-1].lower() for x in Wd.types()]))
        if res:
            event.reply(res)
        else:
            event.reply("no types yet.")
        return
    bot = event.bot()
    otype = event.args[0]
    res = list(find(otype, event.gets))
    if bot.cache:
        if len(res) > 3:
            bot.extend(event.channel, [x[1].txt for x in res])
            bot.say(event.channel, "%s left in cache, use !mre to show more" % bot.cache.size())
            return
    _nr = 0
    for _fn, obj in res:
        txt = "%s %s %s" % (
                            str(_nr),
                            format(obj, event.sets.keys or keys(obj), event.toskip),
                            elapsed(time.time()-fntime(_fn))
                           )
        _nr += 1
        event.reply(txt)
    if not _nr:
        event.reply("no result")
