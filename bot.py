import discord
from discord.ext import commands
from classes.Event import Event

client = commands.Bot(command_prefix='.')
id_increment = 0
events = {}
servers = {}

def check_events_server(ctx):
    return ctx.guild.id in servers


@client.event
async def on_ready():
    print('Bot is ready.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command()
async def begin(ctx, *, event_name):
    global id_increment
    event = Event(id_increment, event_name, ctx.author)
    if not check_events_server(ctx):
        servers[ctx.guild.id] = {}
    server_events = servers[ctx.guild.id]
    server_events[event.id] = event
    id_increment += 1
    await ctx.send(f'{event.host.display_name} started {event.eventName}. Use id {event.id} to enter queue.')


@client.command(aliases=['listq', 'listqueue'])
async def lq(ctx):
    if not check_events_server(ctx):
        embedVar = discord.Embed(title="There are currently no events taking place at this time",
                                 description="Once an admin starts an event you'll find them "
                                             "all listed here!", color=0x902020)
        await ctx.send(embed=embedVar)
    else:
        server_events = servers[ctx.guild.id]
        embedVar = discord.Embed(title="Current events",
                                 description="To ask a question in an event, type `.enter [event_id] [question_topic]`", color=0x902020)
        for event in server_events:
            embedVar.add_field(name=server_events[event].eventName, value=f'Hosted by: {server_events[event].host.display_name}. ID: {server_events[event].id}', inline=False)
        await ctx.send(embed=embedVar)


@client.command(aliases=['q'])
async def queue(ctx, id):
    if not check_events_server(ctx):
        await ctx.send("Sorry, I wasn't able to find any events")
    else:
        server_events = servers[ctx.guild.id]
        event_id = int(id)
        if event_id not in server_events:
            print(server_events)
            await ctx.send("Sorry, I wasn't able to find that event")
        else:
            count = 1
            embedVar = discord.Embed(title=f"{server_events[event_id].eventName}",
                                     description=f"Hosted by: {server_events[event_id].host.display_name}", color=0x902020)
            for entry in server_events[event_id].queue:
                embedVar.add_field(name=f"{count}. {entry.topic}", value=f"Question asked by {entry.author}")
                count += 1
            await ctx.send(embed=embedVar)


@client.command()
async def enter(ctx, id, *, topic):
    if not check_events_server(ctx):
        await ctx.send("Sorry, I wasn't able to find any events")
    else:
        server_events = servers[ctx.guild.id]
        event_id = int(id)
        if event_id not in server_events:
            await ctx.send(f"Sorry, I wasn't able to find any event with ID: {event_id}")
        else:
            server_events[event_id].enter_queue(ctx.author, topic)
            await ctx.send(f"{ctx.author.display_name} was added to queue {event_id}")


@client.command()
async def clear(ctx, id):
    if ctx.guild.id not in servers:
        await ctx.send("Sorry, I wasn't able to find any events")
    else:
        server_events = servers[ctx.guild.id]
        event_id = int(id)
        if event_id not in server_events:
            await ctx.send(f"Sorry, I wasn't able to find any event with ID: {event_id}")
        elif ctx.author != server_events[event_id].host:
            await ctx.send("You are not the host for this event. Only the host can clear the queue for this event.")
        else:
            server_events[event_id].clear_queue()
            await ctx.send(f"The queue has been cleared for {server_events[event_id].eventName}.")

client.run('ODA1MTIwMTc4ODAyMzkzMTA4.YBWQmQ.HynCQfH1FcaRR-ah6UycFOd7sSs')
