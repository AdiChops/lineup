import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

from classes.Event import Event

client = commands.Bot(command_prefix='.')
id_increment = 0
servers = {}

def check_events_server(ctx):
    return ctx.guild.id in servers


@client.event
async def on_ready():
    print('Bot is ready.')

@client.command()
async def ping(ctx):
    """Returns the latency of the bot"""
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command()
@has_permissions(administrator=True)
@commands.has_role('Host')
async def begin(ctx, *, event_name):
    """Only for administrators: begins an even with <event_name>"""
    global id_increment
    event = Event(id_increment, event_name, ctx.author)
    if not check_events_server(ctx):
        servers[ctx.guild.id] = {}
    server_events = servers[ctx.guild.id]
    server_events[event.id] = event
    id_increment += 1
    await ctx.send(f'{event.host.display_name} started {event.eventName}. Use id {event.id} to enter queue.')


@client.command(aliases=['liste', 'listevents'])
async def le(ctx):
    """Lists all events currently taking place"""
    if not check_events_server(ctx):
        embedVar = discord.Embed(title="There are currently no events taking place at this time",
                                 description="Once a host starts an event you'll find them "
                                             "all listed here!", color=0x902020)
        await ctx.send(embed=embedVar)
    else:
        server_events = servers[ctx.guild.id]
        embedVar = discord.Embed(title="Current events",
                                 description="To ask a question in an event, type `.enter [event_id] [question_topic]`", color=0x902020)
        for event in server_events:
            embedVar.add_field(name=server_events[event].eventName, value=f'Hosted by: {server_events[event].host.display_name}. Event ID: {server_events[event].id}. There are currently {len(server_events[event].queue)} in queue', inline=False)
        await ctx.send(embed=embedVar)


@client.command(aliases=['q'])
async def queue(ctx, id):
    """Displays queue for a given <queue_id>"""
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
                embedVar.add_field(name=f"{count}. {entry.topic}",
                                   value=f"Question asked by {entry.author.display_name}", inline=False)
                count += 1
            await ctx.send(embed=embedVar)


@client.command()
async def enter(ctx, id, *, topic="Topic N/A"):
    """Enters a queue with a given <queue_id>"""
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
async def leave(ctx, id, question_id):
    """Leaves the queue with a given <queue_id> and a given <question_id>"""
    if not check_events_server(ctx):
        await ctx.send("Sorry I wasn't able to find any events")
    else:
        server_events = servers[ctx.guild.id]
        event_id = int(id)
        if event_id not in server_events:
            await ctx.send(f"Sorry I wasn't able to find any event with ID: {event_id}")
        else:
            server_events[event_id].leave_queue(ctx.author, int(question_id) - 1)
            await ctx.send(f"{ctx.author.display_name} has left the queue {event_id}")


@client.command()
@has_permissions(administrator=True)
@commands.has_role('Host')
async def clear(ctx, id):
    """Only for administrators: clears the queue of a given <event_id>"""
    if check_events_server(ctx):
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


@client.command()
@has_permissions(administrator=True)
@commands.has_role('Host')
async def end(ctx, id, *, leave_message="Thanks for attending!"):
   """Only for administrators: ends event with id <event_id>"""
   if not check_events_server(ctx):
       await ctx.send("Sorry, I wasn't able to find any events")
   else:
       server_events = servers[ctx.guild.id]
       event_id = int(id)
       if event_id not in server_events:
           await ctx.send(f"Sorry, I wasn't able to find any event with ID: {event_id}")
       elif ctx.author != server_events[event_id].host:
           await ctx.send("You are not the host for this event. Only the host can end their own event.")
       else:
           await ctx.send(f"{ctx.author.display_name}, the host for the event '{server_events[event_id].eventName}' has ended the event!")
           await ctx.send(leave_message)
           server_events.pop(event_id)


@client.command()
@has_permissions(administrator=True)
async def move(ctx, id, old_pos, new_pos):
    if ctx.guild.id  not in servers:
        await ctx.send("Sorry, I wasn't able to find any events")
    else:
        server_events = servers[ctx.guild.id]
        event_id = int(id)
        userToMove = server_events[event_id].queue[int(old_pos)].author.display_name
        if event_id not in server_events:
            await ctx.send(f"Sorry, I wasn't able to find any event with ID: {event_id}")
        elif ctx.author != server_events[event_id].host:
            await ctx.send("You are not the host for this event. Only the host can move people for this event.")
        else:
            server_events[event_id].move_user(int(old_pos), int(new_pos))
            await ctx.send(f"{userToMove} got moved from position {old_pos} to {new_pos}.")

@client.command()
@has_permissions(administrator=True)
async def resolve(ctx, id):
    if not check_events_server(ctx):
        await ctx.send("Sorry, I wasn't able to find any events")
    else:
        server_events = servers[ctx.guild.id]
        event_id = int(id)
        if event_id not in server_events:
            await ctx.send(f"Sorry, I wasn't able to find any event with ID: {event_id}")
        elif ctx.author != server_events[event_id].host:
            await ctx.send("You are not the host for this event. Only the host can resolve for this event.")
        else:
            server_events[event_id].resolve()
            await ctx.send(f"Resolved. {server_events[event_id].currently_served().mention}, you're up next!")


@client.command()
@has_permissions(administrator=True)
async def ready(ctx, id):
    if not check_events_server(ctx):
        await ctx.send("Sorry, I wasn't able to find any events")
    else:
        server_events = servers[ctx.guild.id]
        event_id = int(id)
        if event_id not in server_events:
            await ctx.send(f"Sorry, I wasn't able to find any event with ID: {event_id}")
        elif ctx.author != server_events[event_id].host:
            await ctx.send("You are not the host for this event. Only the host can run this command for this event.")
        else:
            await ctx.send(f"{server_events[event_id].currently_served().mention}, {server_events[event_id].host.display_name} is ready for you!")


client.run('ODA1MTIwMTc4ODAyMzkzMTA4.YBWQmQ.HynCQfH1FcaRR-ah6UycFOd7sSs')
