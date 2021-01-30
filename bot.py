import discord
from classes import Event
from discord.ext import commands

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
async def begin(ctx, *, event_name):
    global id_increment
    event = Event.Event(id_increment, event_name, ctx.author)
    events.append(event)
    id_increment += 1
    await ctx.send(f'{event.host} started {event.eventName}. Use id {event.id} to enter queue.')



client.run('ODA1MTIwMTc4ODAyMzkzMTA4.YBWQmQ.HynCQfH1FcaRR-ah6UycFOd7sSs')

