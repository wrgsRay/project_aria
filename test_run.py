"""
Python 3.6
@Author: wrgsRay
"""
from discord.ext import commands
from keys import aria_code
import discord

# python3 -m pip install -U https://github.com/Rapptz/discord.py/archive/rewrite.zip
prefix = "?"
bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_ready():
    print("Everything's all ready to go~")


@bot.event
async def on_message(message):
    print("The message's content was", message.content)
    await bot.process_commands(message)


@bot.command()
async def ping(ctx):
    '''
    This text will be shown in the help command
    '''

    # Get the latency of the bot
    latency = bot.latency  # Included in the Discord.py library
    # Send it to the user
    await ctx.send(latency)
    await bot.send_message(ctx.channel, msg)


@bot.command()
async def echo(ctx, *, content: str):
    await ctx.send(content)


bot.run(aria_code)

def main():
    pass


if __name__ == '__main__':
    main()