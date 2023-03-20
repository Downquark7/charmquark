import discord
import openai

from config import token
from config import openaikey
from config import aiprompt

openai.api_key = openaikey

dance = '<a:dance1:779548089547620352><a:dance2:779548089228722187><a:dance3:779548089509740545>'

intents = discord.Intents.default()
client = discord.Client(intents=intents)

client.hist = {}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    aiprompt.append({"role": "system", "content": "<@{0.user.id}> is equivalent to your name".format(client)})
    aiprompt.append({"role": "system", "content": "You can send the torture dance gif from jjba by typing \"" + dance + "\""})
    aiprompt.append({"role": "system", "content": "You receive messages from multiple people in the format of \"name: message\" so you "
                                "can differentiate between people and call them by name"})


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    async with message.channel.typing():
        if message.channel.id not in client.hist:
            client.hist[message.channel.id] = aiprompt.copy()
        client.hist[message.channel.id].append({"role": "user", "content": message.content})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=client.hist[message.channel.id]
        )
        client.hist[message.channel.id].append(
            {"role": "assistant", "content": response['choices'][0]['message']['content']})
        await message.channel.send(response['choices'][0]['message']['content'])

client.run(token)
