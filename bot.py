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
async def begin(ctx, *, event_name):
    global id_increment
    event = Event.Event(id_increment, event_name, ctx.author)
    events.append(event)
    id_increment += 1
    await ctx.send(f'{event.host} started {event.eventName}. Use id {event.id} to enter queue.')

@client.command(aliases=['listq', 'listqueue'])
async def lq(ctx):
    if not events:
        embedVar = discord.Embed(title="There are currently no events taking place at this time",
                                 description="Once an admin starts an event you'll find them "
                                             "all listed here!", color=0x902020)
        await ctx.send(embed=embedVar)
    else:
        embedVar = discord.Embed(title="Current events",
                                 description="To ask a question in an event type .enter [event_id]", color=0x902020)
        for event in events:
            embedVar.add_field(name=event.eventName, value=f'Hosted by: {event.host}. ID: {event.id}', inline=False)
        await ctx.send(embed=embedVar)

@client.command()
async def queue(ctx, id):
    for event in events:
        if event.id == id:
            embedVar = discord.Embed(title="Queue " + id, description="User 1\n User 2\nUser 3")
    await ctx.send(embed=embedVar)

client.run('ODA1MTIwMTc4ODAyMzkzMTA4.YBWQmQ.HynCQfH1FcaRR-ah6UycFOd7sSs')

