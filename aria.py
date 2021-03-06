"""
Python 3.6
@Author: wrgsRay
"""
# Documents for discord py: https://discordpy.readthedocs.io/en/rewrite/index.html
# Documents for aiohttp https://docs.aiohttp.org/en/stable/client_advanced.html#custom-request-headers
# Documents for aiohttp https://docs.aiohttp.org/en/stable/client_reference.html

import aiohttp
import discord
from discord.ext import commands
import asyncio
from keys import aria_code, dark_sky_API_key, alpha_vantage_key
import random
from time import time
from bs4 import BeautifulSoup as bs
import re


def main():
    # Set prefix and remove default help command
    bot = commands.Bot(command_prefix='!')
    bot.remove_command('help')
    start_time = time()
    activity = discord.Game(name="!help for help")

    # Print something to console once logged in
    @bot.event
    async def on_ready():
        # channel = bot.get_channel(308155307165483009)
        channel = bot.get_channel(372977988322721794)
        print('We have logged in as {0.user}'.format(bot))
        await channel.send('Aria, up and running.')
        await bot.change_presence(status=discord.Status.idle, activity=activity)

    @bot.event
    async def on_message(message):
        print("The message's content was", message.content)
        # TODO: do something when detected

        await bot.process_commands(message)

    # commands
    @bot.command()
    async def help(ctx):
        """Display help"""
        embed = discord.Embed(title='Aria', description='Simple bot for personal use:', color=0xeee657)

        embed.add_field(name='!plus <X> <Y>', value='Aria calculates and gives the sum of X and Y')
        embed.add_field(name='!multiply <X> <Y>', value='Aria calculates and gives the product of X and Y')
        embed.add_field(name='!greet', value='Aria greets you.')
        embed.add_field(name='!choose <A> <B> <C> <D>',
                        value='Aria makes a choice for you out of the things you give her.')
        embed.add_field(name='!sam', value='(disabled) Aria pulls the price of regular gasoline of Sam\'s Club, El Monte')
        embed.add_field(name='!remindme <5m> <pizza>',
                        value='Aria reminds you after a certain time. Type the command for usage.')
        embed.add_field(name='!weather <location>',
                        value='Aria tells you the current and weekly forecast for the a location')

        await ctx.send(embed=embed)

    @bot.command()
    async def info(ctx):
        """Display basic info of bot"""
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
        """Addition command"""
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

    @bot.command(decription='check price on Sam\'s Club')
    async def sam(ctx):
        url = 'https://www.gasbuddy.com/station/119637'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                body = await r.text(encoding='utf-8')
                soup = bs(body, 'html.parser')
        price = soup.find('h1', {'class': 'header__header1___3U_VP header__header___1zII0 styles__price___1wJ_R'}).text
        updated = soup.find('div', {'class': 'styles__reportedTime___EIf9S'}).text
        await ctx.send(f'{ctx.message.author.mention} '
                       f'Latest Price from Sam\'s Club for regular gasoline is {price} and it is updated {updated}.')

    @bot.command()
    async def fuck(ctx):
        await ctx.send(f'{ctx.message.author.mention} you baka!')

    @bot.command()
    async def remindme(ctx, duration='empty', *comments):
        re_day = re.compile('^\dd')
        re_min = re.compile('^\d{1,4}m')
        re_sec = re.compile('^\d{1,4}s')
        if duration == 'empty':
            await ctx.send(f'{ctx.message.author.mention} To use: !remindme XXd/XXm/XXs [comments] '
                           'eg. !remindme 5s hello for 5 second reminder with comments as "hello"')
        elif re_day.match(duration):
            days = int(duration[:1])
            if days:
                await ctx.send(f'{ctx.message.author.mention} Sorry. Reminder for days is disabled for now.')
            # if days < 5:
            #     await ctx.send(f'{ctx.message.author.mention} Your reminder is set for {days} day(s)!')
            #     await asyncio.sleep(1 * days)
            #     # await asyncio.sleep(86400 * days)
            #     await ctx.send(f'{ctx.message.author.mention} Beep Beep! '
            #                    f'I\'m here to remind you: ' + ' '.join(comments))
            else:
                await ctx.send(f'{ctx.message.author.mention} Sorry! I have short memories. Please try a shorter time.')
        elif re_min.match(duration):
            minutes = int(duration[:len(duration) - 1])
            if minutes < 1000:
                await ctx.send(f'{ctx.message.author.mention} Your reminder is set for {minutes} minute(s)!')
                await asyncio.sleep(60 * minutes)
                await ctx.send(f'{ctx.message.author.mention} Beep Beep! '
                               f'I\'m here to remind you: ' + ' '.join(comments))
            else:
                await ctx.send(f'{ctx.message.author.mention} Sorry! I have short memories. Please try a shorter time.')
        elif re_sec.match(duration):
            seconds = int(duration[:len(duration) - 1])
            if seconds < 3600:
                await ctx.send(f'{ctx.message.author.mention} Your reminder is set for {seconds} second(s)!')
                await asyncio.sleep(seconds)
                await ctx.send(f'{ctx.message.author.mention} Beep Beep! '
                               f'I\'m here to remind you: ' + ' '.join(comments))
            else:
                await ctx.send(f'{ctx.message.author.mention} Sorry! I have short memories. Please try a shorter time.')
        else:
            await ctx.send(f'{ctx.message.author.mention} Sorry! I do not understand that duration. '
                           f'To use: !remindme XXd/XXm/XXs [comments] '
                           f'eg. !remindme 5s hello for 5 second reminder with comments as "hello"')

    @bot.command()
    async def weather(ctx, *location):
        fixed_location = ' '.join(location)
        if not location:
            await ctx.send('To use, do !weather Location. Eg. !weather Los Angeles')
        else:
            geocoding_url = 'https://nominatim.openstreetmap.org/search/%s?format=json&polygon=0&addressdetails=0' \
                            % fixed_location
            async with aiohttp.ClientSession() as session:
                async with session.get(geocoding_url) as resp:
                    coordinates_dict = await resp.json()
            coordinates = coordinates_dict[0]['lat'] + ',' + coordinates_dict[0]['lon']

            weather_url = 'https://api.darksky.net/forecast/%s/%s' % (dark_sky_API_key, coordinates)
            async with aiohttp.ClientSession() as session:
                async with session.get(weather_url) as resp:
                    d = await resp.json()
            await ctx.send(f'The current temperature in {coordinates_dict[0]["display_name"]}'
                           f' is {d["currently"]["temperature"]} °F\n'
                           f'The current forecast is: {d["daily"]["summary"]}')

    @bot.command()
    async def stock(ctx, symbol = 'empty'):
        if symbol == 'empty':
            await ctx.send('Give me a symbol')
        else:
            stock_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}' \
                f'&interval=1min&apikey={alpha_vantage_key}'
            async with aiohttp.ClientSession() as session:
                async with session.get(stock_url) as resp:
                    d = await resp.json()
                    meta_symbol = d['Meta Data']['2. Symbol']
                    latest = d['Meta Data']['3. Last Refreshed']
                    close_price = d['Time Series (1min)'][latest]['4. close']
            await ctx.send(f'At {latest}, the closing price for {meta_symbol} is {close_price}')

    @bot.command()
    async def uptime(ctx):
        now = time()
        difference = int(now - start_time)
        hours = difference // 3600
        minutes = (difference - 3600 * hours) // 60
        seconds = difference % 60
        await ctx.send(f'I have been up for {hours} hours, {minutes} minutes and {seconds} seconds.')

    @bot.command()
    async def communityday(ctx):
        community_day_url = 'https://pokemongolive.com/en/events/community-day/americas/'
        async with aiohttp.ClientSession() as session:
            async with session.get(community_day_url) as r:
                body = await r.text(encoding='utf-8')
                soup = bs(body, 'html.parser')
                raw_values = soup.find_all('div', class_='communityday__hero__bubble__label')
                titles = list()
                for i in raw_values:
                    titles.append(i.get_text())
                raw_values = soup.find_all('div', class_='communityday__hero__bubble__value')
                values = list()
                for i in raw_values:
                    values.append(i.get_text())
                zipped = list(zip(titles, values))
                embed = discord.Embed(title='Community Day', color=0xeee657)
                for i in zipped:
                    embed.add_field(name=i[0], value=i[1])
                embed.add_field(name='For more info:',
                                value='Go to https://pokemongolive.com/en/events/community-day/americas/')

        await ctx.send(embed=embed)

    bot.run(aria_code)


if __name__ == '__main__':
    main()
