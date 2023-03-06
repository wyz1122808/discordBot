import discord
from discord.ext import commands
import pandas as pd
import numpy as np
import datetime as dt
import asyncio
from time import sleep
import os



intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix='tc ', intents=intents)
path = './image/'
gift = ["土豆泥", "通心面", "肉汁", "玉米粒", "糖甜薯", "苹果派"]
# admin manual:
manual = "管理员使用手册：\n"


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  print('版本信息：')
  print('Beta 1.0 \n ')


@client.event
async def on_message(message):

  channel = message.channel
  if message.content == "tc manual":
    await channel.send(
      "管理员使用手册：\n 1.抽奖指令： 心怀感恩，所遇皆温柔！ TC感谢每一位相遇的你们！ \n 2.查询所有用户获奖情况指令：tc stat  \n 3.查询指定用户获奖情况： 输入指令 [tc chaxun ] + 用户ID 。 \n  例如： tc chaxun 717898166011297842 \n注：若要查询用户ID，在DISCORD设置中找到高级设置，打开开发者模式。右键点击用户头像即可复制ID。\n 请在私密频道使用，指令不得被非管理员使用。"
    )

  if message.content == "tc stat":
    df = pd.read_csv('data1.csv')
    t = ""
    length = len(df.index)
    m = 0
    mm = 0
    for j in range(1, 10):
      k = m
      for i in range(k, k+34):
        num = df.iloc[i, 0]
        user = message.guild.get_member(int(num))
        name = user.name
        t += f"名字： {name} : 土豆泥：{int(df.iloc[i, 2])}  通心面：{int(df.iloc[i, 3])} 肉汁：{int(df.iloc[i, 4])}  玉米粒：{int(df.iloc[i, 5])}  糖甜薯：{int(df.iloc[i, 6])} 苹果派：{int(df.iloc[i, 7])}  \n"
        if i == length -1 :
          mm = 1
          break
        
      await channel.send(t)
      if mm == 1:
        break
      t = ""
      m += 35

  if message.content == '心怀感恩，所遇皆温柔！ TC感谢每一位相遇的你们！':
    print(f"type of input id:{type(message.author.id)}")

    def available(sid):
      id = str(sid)
      now = dt.datetime.now()
      df = pd.read_csv('data1.csv')
      found = 0

      for i in range(0, len(df.index)):
        
        if str(df.iloc[i, 0]) == str(id):
          found = 1
          position = i
          print('found id in data')
      # new user into database
      if found == 0:
        print('new id detected, creating new row...')
        index = len(df.index)
        print('creating new row in {}'.format(index))
        new = {
          'client1': str(id),
          'timestamp': now,
          'value1': 0,
          'value2': 0,
          'value3': 0,
          'value4': 0,
          'value5': 0,
          'value6': 0
        }
        df = df.append(new, ignore_index=True)
        print(f"putting new ID into dataset, type is {type(new['client1'])}")
        df.to_csv('data1.csv', index=False)
        return [1, index]
      #old user, check for time stamps
      else:
        pos = df.iloc[position, 1]
        a = pos
        c = now - dt.datetime.strptime(a, "%Y-%m-%d %H:%M:%S.%f")

        inmin = c.seconds / 60
        if c.days > 0 or inmin >= 120:
          return [1, position]
        else:
          remain = 0
          if inmin < 120:
            remain = inmin
            return [0, 120 - remain]
          else:

            return [0, 1440 - inmin]

    def update(time, gain, position):
      
      now = dt.datetime.now()

      df = pd.read_csv('data1.csv')
      df.iloc[position, 1] = dt.datetime.strftime(now, "%Y-%m-%d %H:%M:%S.%f")
      df.iloc[position, gain + 1] += 1
      df.iloc[position, gain + 1] = int(df.iloc[position, gain + 1])
      df.to_csv('data1.csv', index=False)

      return

    current = np.random.choice(np.arange(1, 7))
    channel = message.channel
    res = available(message.author.id)
    name = message.author.name
    embed = discord.Embed(title=f"恭喜  {name}  抽到了 {gift[current-1]} 卡!",
                          description=" ",
                          color=0xFF5733)
    file = discord.File(f"./image/{current}.png", filename="image.png")
    embed.set_image(url="attachment://image.png")
    if res[0] == 1:
      update(dt.datetime.now(), current, res[1])
      await channel.send(file=file, embed=embed)
    else:
      await channel.send(f'还有{int(res[1])}分钟后才能进行下一次抽奖鸭~')
  await client.process_commands(message)


@client.command(name="chaxun")
async def _chaxun(ctx, msg):
  

  df = pd.read_csv('data1.csv')
  f = 0
  t = ""
  for i in range(0, len(df.index)):
    a = df.iloc[i, 0]
    if str(a) == msg:
      f = 1
      user = ctx.message.guild.get_member(int(df.iloc[i, 0]))
      name = user.name
      t += f"名字： {name} : 土豆泥：{df.iloc[i, 2]}  通心面：{df.iloc[i, 3]} 肉汁：{df.iloc[i, 4]}  玉米粒：{df.iloc[i, 5]}  糖甜薯：{df.iloc[i, 6]} 苹果派：{df.iloc[i, 7]}  \n"

  if f == 0:
    t = '该用户没有任何卡片'
  await ctx.send(t)







while __name__ == '__main__':
  try:
    
    client.run(
  'MTAzODIwOTQ0MDM3NTExOTk1NQ.GCFvpp.YRfzYx7pRTo8uTYGqtQZxED0r7p_EQgeIylc7Y')
  except discord.errors.HTTPException as e:
    print(e)
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    os.system('kill 1')