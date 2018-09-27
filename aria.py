"""
Python 3.6
@Author: wrgsRay
"""
import discord
from discord.ext import commands
import asyncio
from keys import aria_code
import random
import requests
from bs4 import BeautifulSoup as bs


def main():
    bot = commands.Bot(command_prefix='!')

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

    @bot.command(description='check price on Sam\'s Club')
    async def sam(ctx):
        """Check and return price of Sam's Club"""
        s = requests.get('https://www.gasbuddy.com/station/119637')
        soup = bs(s.text, 'html.parser')
        price = soup.find('h1', {'class': 'style__header1___1jBT0 style__header___onURp styles__price___1wJ_R'}).text
        updated = soup.find('div', {'class': 'styles__reportedTime___EIf9S'}).text
        await ctx.send(f'{ctx.message.author.mention} '
                       f'Latest Price from Sam\'s Club for regular gasoline is {price} and it is updated {updated}.')

    bot.run(aria_code)


if __name__ == '__main__':
    main()
