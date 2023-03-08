import discord
import requests
import os
import re
import math
import sys
import linecache
import uwuifier.uwuify as uwu
import openai
from wakeonlan import send_magic_packet
from datetime import datetime
from PIL import Image
from datetime import datetime, timedelta

from config import token
from config import postsUrl
from config import weatherUrl
from config import forecastUrl
from config import openaikey
from config import apiprompt

openai.api_key = openaikey

timeformat = "%A %I:%M%p"

COOLDOWN = 2


def get_exception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


dance = '<a:dance1:779548089547620352><a:dance2:779548089228722187><a:dance3:779548089509740545>'

intents = discord.Intents.default()
# intents.message_content = True
client = discord.Client(intents=intents)

client.agreeCounter = 0

asciilogo = os.popen('screenfetch -N -L').read().replace("`", "'")

client.hist = {}

client.last_response_time = datetime.now() - timedelta(minutes=COOLDOWN + 1)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    aiprompt.append({"role": "system", "content": "<@{0.user.id}> is your name".format(client)})


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!spam'):
        async with message.channel.typing():
            for i in range(10):
                await message.channel.send((message.content[6:]).replace('!dance', dance))

    # if message.content.startswith('$hello'):
    #     await message.channel.send('Hello!')
    #
    # if message.content.startswith('bandapp'):
    #     ms = requests.get(postsUrl).json()["result_data"]["items"][0]["content"]
    #     await message.channel.send(ms)

    if message.content.startswith('resethistory'):
        client.hist = {}
        await message.channel.send('history deleted')

    if client.user.mentioned_in(message):
        async with message.channel.typing():
            if message.channel.id not in client.hist:
                client.hist[message.channel.id] = aiprompt.copy()
            client.hist[message.channel.id].append({"role": "user", "content": message.content})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=client.hist[message.channel.id],
                max_tokens=64
            )
            client.hist[message.channel.id].append(
                {"role": "assistant", "content": response['choices'][0]['message']['content']})
            await message.channel.send(response['choices'][0]['message']['content'])
    # if message.content.startswith('weather'):
    #     ms = ""
    #     weather = requests.get(weatherUrl).json()
    #     temp = str(round((weather['main']['temp'] - 273.15) * 9.0 / 5 + 32, 1))
    #     ms += 'It is currently ' + temp + '°F with a '
    #     ms += weather['weather'][0]['description']
    #     await message.channel.send(ms)
    #
    # if message.content.startswith('agree'):
    #     client.agreeCounter += 1
    #     if (client.agreeCounter == 5):
    #         client.agreeCounter = 0
    #         await message.channel.send('stop.')
    # else:
    #     client.agreeCounter = 0
    #
    # if message.content.startswith('forecast'):
    #     forecast = requests.get(forecastUrl).json()
    #     hourly = forecast['hourly']
    #     ms = ''
    #     for hour in hourly:
    #         timestamp = datetime.fromtimestamp(hour['dt'])
    #         if timestamp.hour == 17:
    #             temp = str(round((hour['temp'] - 273.15) * 9.0 / 5 + 32, 1))
    #             ms += 'On ' + timestamp.strftime(timeformat) + ' it will be ' + temp + '°F with a '
    #             ms += hour['weather'][0]['description'] + '\n'
    #         if timestamp.hour == 18:
    #             temp = str(round((hour['temp'] - 273.15) * 9.0 / 5 + 32, 1))
    #             ms += 'On ' + timestamp.strftime(timeformat) + ' it will be ' + temp + '°F with a '
    #             ms += hour['weather'][0]['description'] + '\n'
    #             ms += 'Sounds like a GREAT day for band!'
    #             await message.channel.send(ms)
    #             break
    if message.content.startswith('fortune'):
        # print("fortune triggered")
        await message.channel.send(os.popen('/usr/games/fortune').read())

    # if message.content.startswith('!meme'):
    #    await message.channel.send('!meme ' + os.popen('fortune -s').read())

    # if message.content.startswith('!generatememe'):
    #    await message.channel.send('!generatememe ' + os.popen('fortune -s').read())

    if message.content.startswith('whoami'):
        await message.channel.send(os.popen('whoami').read())

    if message.content.startswith('!vote'):
        await message.channel.send(
            '. 　。　　　　•　 　ﾟ　　。 　　.\n　　　.　　　 　　.　　　　　。　　 。　. 　.　\n　 。　 ඞ 。　 . • . ' +
            message.content[6:] + ' was ejected. . .\n 　 。　. 　 　　。　　　　　　\nﾟ　　　.　　　　　. ,　　　　.　 .　　 .')

    if message.content.lower().startswith('what is love'):
        await message.channel.send('baby don\'t hurt me')

    if message.content.startswith('kinematics'):
        if len(message.content) == len('kinematics'):
            await message.channel.send("format is kinematics p=(x0,y0) v=(v@a) or v=(vx,vy) target=(x/y/t=0)")
        else:
            try:
                p = (0, 0)
                v = (0, 0)
                a = -9.80

                target = 't'
                targetNum = 0

                m = re.search("unit=ft", message.content)
                if m:
                    a = -32.174

                m = re.search("p=\((-?\d*\.?\d*), ?(-?\d*\.?\d*)\)", message.content)
                if m:
                    print(m.group(0))
                    p = (float(m.group(1)), float(m.group(2)))
                    print(p)

                m = re.search("v=\((-?\d*\.?\d*), ?(-?\d*\.?\d*)\)", message.content)
                if m:
                    print(m.group(0))
                    v = (float(m.group(1)), float(m.group(2)))
                    print(v)

                m = re.search("v=\((-?\d*\.?\d*)@(-?\d*\.?\d*)\)", message.content)
                if m:
                    print(m.group(0))
                    v = (math.cos(math.radians(float(m.group(2)))) * float(m.group(1)),
                         math.sin(math.radians(float(m.group(2)))) * float(m.group(1)))
                    print(v)

                m = re.search("target=\(?(x?y?t?)=(-?\d*\.?\d*)\)?", message.content)
                if m:
                    print(m.group(0))
                    target = m.group(1)
                    targetNum = float(m.group(2))

                if target == 't':
                    t = targetNum
                    x = v[0] * t + p[0]
                    y = (0.5 * a * t * t) + (v[1] * t) + (p[1])
                    print(t)
                    t = round(t, 5)
                    x = round(x, 5)
                    y = round(y, 5)
                    await message.channel.send(message.content + ": \n"
                                                                 "(" + str(x) + ", " + str(y) + ") @ " + str(t) + "s")

                if target == 'y':
                    t = -(math.sqrt(v[1] * v[1] + 2 * a * (targetNum - p[1])) + v[1]) / a
                    x = v[0] * t + p[0]
                    y = (0.5 * a * t * t) + (v[1] * t) + (p[1])
                    print(t)
                    t = round(t, 5)
                    x = round(x, 5)
                    y = round(y, 5)
                    await message.channel.send(message.content + ": \n"
                                                                 "(" + str(x) + ", " + str(y) + ") @ " + str(t) + "s")

                if target == 'x':
                    t = (targetNum - p[0]) / v[0]
                    x = v[0] * t + p[0]
                    y = (0.5 * a * t * t) + (v[1] * t) + (p[1])
                    print(t)
                    t = round(t, 5)
                    x = round(x, 5)
                    y = round(y, 5)
                    await message.channel.send(message.content + ": \n"
                                                                 "(" + str(x) + ", " + str(y) + ") @ " + str(t) + "s")
            except Exception:
                await message.channel.send("Oh no, I threw an error! <@195641705981018112>")
                await message.channel.send("```" + get_exception() + "```")
                print(get_exception())

    if message.content.startswith('!dance'):
        await message.channel.send(
            '<a:dance1:779548089547620352><a:dance2:779548089228722187><a:dance3:779548089509740545>')

    if message.content.startswith('speedtest'):
        async with message.channel.typing():
            await message.channel.send('```' + os.popen('speedtest').read() + '```')

    if message.content.startswith('!status'):
        await message.channel.send('```' + asciilogo + os.popen("screenfetch -N -n -d '-host'").read() + '```')

    if message.content.startswith('!ascii'):
        async with message.channel.typing():
            if len(message.attachments) > 0:  # If the user included an image
                filename = '/home/enicely/lastimage'
                await message.attachments[0].save(filename)
                im1 = Image.open(filename).convert('RGB')
                im1.save(filename + '.jpg')
                await message.channel.send('```' + os.popen('jp2a ' + filename + '.jpg --width=44').read() + '```')

    if message.content.startswith('uwu') or message.content.startswith('owo'):
        await message.channel.send(uwu.uwuify_string(message.content[4:]))

    if message.content.lower().startswith('agree') and (
            (datetime.now() - client.last_response_time) > timedelta(minutes=COOLDOWN)):
        await message.channel.send('Agree')
        client.last_response_time = datetime.now()

    # if message.content.startswith('!print'):
    # with open('pic1.jpg', 'wb') as handle:
    # response = requests.get('http://localhost:8080/?action=snapshot', stream=True)
    # if not response.ok:
    # print(response)
    # for block in response.iter_content(1024):
    # if not block:
    # break
    # handle.write(block)
    # img1 = Image.open('pic1.jpg')
    # img2 = img1.rotate(180, expand=True)
    # img2.save('pic2.jpg')
    # await message.channel.send(file=discord.File('pic2.jpg'))


client.run(token)
