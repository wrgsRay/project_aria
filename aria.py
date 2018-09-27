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
    bot.remove_command('help')

    @bot.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(bot))

    @bot.command()
    async def help(ctx):
        embed = discord.Embed(title='Aria', description='Simple bot for personal use:', color=0xeee657)

        embed.add_field(name='!plus X Y', value='Aria calculates and gives the sum of X and Y')
        embed.add_field(name='!multiply X Y', value='Aria calculates and gives the product of X and Y')
        embed.add_field(name='!greet', value='Aria greets you.')
        embed.add_field(name='!choose', value='Aria makes a choice for you out of the things you give her.')
        embed.add_field(name='!sam', value='Aria pulls the price of regular gasoline of Sam\'s Club, El Monte')

        await ctx.send(embed=embed)

    @bot.command()
    async def info(ctx):
        embed = discord.Embed(title="Aria", description="Simple bot for personal use", color=0xeee657)

        # give info about you here
        embed.add_field(name="Author", value="wrgs(Ray)")

        # Shows the number of servers the bot is member of.
        embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

        # give users a link to invite thsi bot to their server
        # embed.add_field(name="Invite", value="[Invite link](<insert your OAuth invitation link here>)")

        await ctx.send(embed=embed)

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
        await ctx.send(f'Product of {a} and {b} is {a * b}')

    @bot.command()
    async def greet(ctx):
        await ctx.send(f"{ctx.message.author.mention} :smiley: お帰りなさい")

    @bot.command(description='For when you wanna settle the score some other way')
    async def choose(ctx, *choices: str):
        """Chooses between multiple choices."""

        await ctx.send(f'I choose {random.choice(choices)}')

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
