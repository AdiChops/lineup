import discord
from classes import Event
from discord.ext import commands

from classes.Event import Event

ids = 0

client = commands.Bot(command_prefix = '.')
id_increment = 0
events = []

@client.event
async def on_ready():
    print('Bot is ready.')


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def begin(ctx):
    global id_increment
    event = Event.Event(id_increment, "random name")
    events.append(event)
    id_increment += 1
    await ctx.send(f'Someone started {event.eventName}. Use id {event.id} to enter queue.')

@client.command(aliases=['listq', 'listqueue'])
async def lq(ctx):
    embedVar = discord.Embed(title="Test", description="")
    await ctx.send(embed=embedVar)

client.run('ODA1MTIwMTc4ODAyMzkzMTA4.YBWQmQ.HynCQfH1FcaRR-ah6UycFOd7sSs')

