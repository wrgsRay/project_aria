"""
Python 3.6
@Author: wrgsRay
"""
import discord
from discord.ext import commands
import asyncio
from keys import aria_code


def plus(first, second):
    try:
        int(first)
    except ValueError:
        return 'invalid input 1'
    try:
        int(second)
    except ValueError:
        return 'invalid input 2'
    else:
        return int(first) + int(second)


def main():
    client = discord.Client()

    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('-------')
        print(plus(1, 2))

    @client.event
    async def on_message(message):
        # We do not want the bot to respond to itself
        if message.author == client.user:
            return

        if message.content.startswith('!hello'):
            msg = 'Hello {0.author.mention}'.format(message)
            await client.send_message(message.channel, msg)

    client.run(aria_code)


if __name__ == '__main__':
    main()
