"""
Python 3.6
@Author: wrgsRay
"""
import discord
from discord.ext import commands
import asyncio
from keys import aria_code


def main():
    client = discord.Client()

    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('-------')

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
