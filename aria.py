"""
Python 3.6
@Author: wrgsRay
"""
import discord
from discord.ext import commands
import asyncio
from keys import aria_code
import random


def main():
    bot = commands.Bot(command_prefix='$')

    @bot.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(bot))

    @bot.command()
    async def plus(ctx, first, second):
        try:
            int(first)
        except ValueError:
            await ctx.send('Error: Invalid Input')
        try:
            int(second)
        except ValueError:
            await ctx.send('Error: Invalid Input')
        else:
            sum = int(first) + int(second)
            await ctx.send(f'Sum of {first} and {second} is {sum}')

    @bot.command()
    async def multiply(ctx, a: int, b: int):
        await ctx.send(a * b)

    @bot.command()
    async def greet(ctx):
        await ctx.send(f"{ctx.message.author.mention} smiley: :wave: Hello, there!")

    @bot.command(description='For when you wanna settle the score some other way')
    async def choose(ctx, *choices: str):
        """Chooses between multiple choices."""

        await ctx.send(random.choice(choices))

    bot.run(aria_code)


if __name__ == '__main__':
    main()
