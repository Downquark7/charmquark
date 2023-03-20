import discord
import openai
from config import token
from config import openaikey
from config import aiprompt
import sys
import linecache

openai.api_key = openaikey
dance = '<a:dance1:779548089547620352><a:dance2:779548089228722187><a:dance3:779548089509740545>'
intents = discord.Intents.default()
client = discord.Client(intents=intents)
client.hist = {}


def get_exception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    aiprompt.insert(0, {"role": "system", "content": "<@{0.user.id}> is equivalent to your name".format(client)})
    aiprompt.insert(0,
                    {"role": "system",
                     "content": "You can send the torture dance gif from jjba by typing \"" + dance + "\""})
    aiprompt.insert(0, {"role": "system",
                        "content": "You receive messages from multiple people in the format of \"name: message\" so you "
                                   "can differentiate between people and call them by name"})


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("exit()"):
        exit()

    async with message.channel.typing():
        if message.channel.id not in client.hist:
            client.hist[message.channel.id] = aiprompt.copy()
        client.hist[message.channel.id].append(
            {"role": "user", "content": "<@{0.author.id}>: ".format(message) + message.content})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=client.hist[message.channel.id],
            max_tokens=100
        )
        print(response['usage']['total_tokens'])
        if response['usage']['total_tokens'] > 3000:
            client.hist[message.channel.id] = aiprompt.copy()
            client.hist[message.channel.id].append(
                {"role": "user", "content": "<@{0.author.id}>: ".format(message) + message.content})
            await message.channel.send("Message history cleared nya~")
        client.hist[message.channel.id].append(
            {"role": "assistant", "content": response['choices'][0]['message']['content']})
        await message.channel.send(response['choices'][0]['message']['content'])


client.run(token)
