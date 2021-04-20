import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import sys

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
    print(f"Ping command sent from server: {ctx.message.guild.name} by {ctx.message.author}")
    sys.stdout.flush()
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command()
@commands.has_role('Host')
async def begin(ctx, *, event_name):
    """Only for hosts: begins an even with <event_name>"""
    print(f"Begin command sent from server: {ctx.message.guild.name} by {ctx.message.author}")
    sys.stdout.flush()
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
    print(f"List events command sent from server: {ctx.message.guild.name} by {ctx.message.author}")
    sys.stdout.flush()
    if not check_events_server(ctx) or len(servers[ctx.guild.id]) == 0:
        embed_var = discord.Embed(title="There are currently no events taking place at this time",
                                  description="Once a host starts an event you'll find them "
                                              "all listed here!", color=0x902020)
        await ctx.send(embed=embed_var)
    else:
        server_events = servers[ctx.guild.id]
        embed_var = discord.Embed(title="Current events",
                                  description="To ask a question in an event, type "
                                              "`.enter [event_id] [question_topic]`",
                                  color=0x902020)
        for event in server_events:
            embed_var.add_field(name=server_events[event].eventName,
                                value=f'Hosted by: {server_events[event].host.display_name}. '
                                f'Event ID: {server_events[event].id}. '
                                f'There are currently {len(server_events[event].queue)} in queue', inline=False)
        await ctx.send(embed=embed_var)


@client.command(aliases=['q'])
async def queue(ctx, eid):
    """Displays queue for a given <queue_id>"""
    print(f"Queue command sent from server: {ctx.message.guild.name} by {ctx.message.author}")
    sys.stdout.flush()
    if not check_events_server(ctx):
        await ctx.send("Sorry, I wasn't able to find any events")
    else:
        server_events = servers[ctx.guild.id]
        event_id = int(eid)
        if event_id not in server_events:
            print(server_events)
            await ctx.send("Sorry, I wasn't able to find that event")
        else:
            count = 1
            embed_var = discord.Embed(title=f"{server_events[event_id].eventName}",
                                      description=f"Hosted by: {server_events[event_id].host.display_name}",
                                      color=0x902020)

            for entry in server_events[event_id].queue:
                embed_var.add_field(name=f"{count}. {entry.topic}",
                                    value=f"Question asked by {entry.author.display_name}", inline=False)
                count += 1
            await ctx.send(embed=embed_var)


@client.command()
async def enter(ctx, eid, *, topic="Topic N/A"):
    """Enters a queue with a given <queue_id>"""
    print(f"Enter command sent from server: {ctx.message.guild.name} by {ctx.message.author}")
    sys.stdout.flush()
    if not check_events_server(ctx):
        await ctx.send("Sorry, I wasn't able to find any events")
    else:
        server_events = servers[ctx.guild.id]
        event_id = int(eid)
        if event_id not in server_events:
            await ctx.send(f"Sorry, I wasn't able to find any event with ID: {event_id}")
        else:

            await ctx.send(f"{ctx.author.display_name} was added to queue {event_id}"
                           if server_events[event_id].enter_queue(ctx.author, topic) else
                           "You've exceeded the maximum amount of question in a queue, wait for the host "
                           "to resolve one of your questions")


@client.command()
async def leave(ctx, eid, question_id):
    """Leaves the queue with a given <queue_id> and a given <question_id>"""
    print(f"Leave command sent from server: {ctx.message.guild.name} by {ctx.message.author}")
    sys.stdout.flush()
    if not check_events_server(ctx):
        await ctx.send("Sorry I wasn't able to find any events")
    else:
        server_events = servers[ctx.guild.id]
        event_id = int(eid)
        if event_id not in server_events:
            await ctx.send(f"Sorry I wasn't able to find any event with ID: {event_id}")
        else:
            current = server_events[event_id].get_question_at(int(question_id) - 1)
            if current.author != ctx.author:
                await ctx.send("You can only remove yourself from the queue")
            else:
                server_events[event_id].resolve(int(question_id) - 1)
                await ctx.send(f"{ctx.author.display_name} has left the queue {event_id}")


@client.command()
@commands.has_role('Host')
async def clear(ctx, eid):
    """Only for hosts: clears the queue of a given <event_id>"""
    print(f"Clear command sent from server: {ctx.message.guild.name} by {ctx.message.author}")
    sys.stdout.flush()
    if not check_events_server(ctx):
        await ctx.send("Sorry, I wasn't able to find any events")
    else:
        server_events = servers[ctx.guild.id]
        event_id = int(eid)
        if event_id not in server_events:
            await ctx.send(f"Sorry, I wasn't able to find any event with ID: {event_id}")
        elif ctx.author != server_events[event_id].host:
            await ctx.send("You are not the host for this event. Only the host can clear the queue for this event.")
        else:
            server_events[event_id].clear_queue()
            await ctx.send(f"The queue has been cleared for {server_events[event_id].eventName}.")


@client.command()
@commands.has_role('Host')
async def end(ctx, eid, *, leave_message="Thanks for attending!"):
    """Only for hosts: ends event with id <event_id>"""
    print(f"End command sent from server: {ctx.message.guild.name} by {ctx.message.author}")
    sys.stdout.flush()
    if not check_events_server(ctx):
        await ctx.send("Sorry, I wasn't able to find any events")
    else:
        server_events = servers[ctx.guild.id]
        event_id = int(eid)
        if event_id not in server_events:
            await ctx.send(f"Sorry, I wasn't able to find any event with ID: {event_id}")
        elif ctx.author != server_events[event_id].host:
            await ctx.send("You are not the host for this event. Only the host can end their own event.")
        else:
            await ctx.send(f"{ctx.author.display_name}, the host for the event"
                           f" '{server_events[event_id].eventName}' has ended the event!")
            await ctx.send(leave_message)
            server_events.pop(event_id)


@client.command()
@commands.has_role('Host')
async def move(ctx, eid, old_pos, new_pos):
    """Only for hosts: Moves person at <old_position> to <new_position> with event id <event_id>"""
    print(f"Move command sent from server: {ctx.message.guild.name} by {ctx.message.author}")
    sys.stdout.flush()
    if ctx.guild.id not in servers:
        await ctx.send("Sorry, I wasn't able to find any events")
    else:
        server_events = servers[ctx.guild.id]
        event_id = int(eid)
        user_to_move = server_events[event_id].queue[int(old_pos) - 1].author.display_name
        if event_id not in server_events:
            await ctx.send(f"Sorry, I wasn't able to find any event with ID: {event_id}")
        elif ctx.author != server_events[event_id].host:
            await ctx.send("You are not the host for this event. Only the host can move people for this event.")
        else:
            server_events[event_id].move_user(int(old_pos) - 1, int(new_pos) - 1)
            await ctx.send(f"{user_to_move} got moved from position {old_pos} to {new_pos}.")


@client.command()
@commands.has_role('Host')
async def resolve(ctx, eid, question_index=1):
    """Only for hosts: Resolves current user's question
    (or question at index <index>) and mentions next user in queue"""
    print(f"Resolve command sent from server: {ctx.message.guild.name} by {ctx.message.author}")
    sys.stdout.flush()
    if not check_events_server(ctx):
        await ctx.send("Sorry, I wasn't able to find any events")
    else:
        server_events = servers[ctx.guild.id]
        event_id = int(eid)
        if event_id not in server_events:
            await ctx.send(f"Sorry, I wasn't able to find any event with ID: {event_id}")
        elif ctx.author != server_events[event_id].host:
            await ctx.send("You are not the host for this event. Only the host can resolve for this event.")
        else:
            server_events[event_id].resolve(int(question_index) - 1)
            await ctx.send(f"Resolved. {server_events[event_id].currently_served().mention}, you're up next!")


@client.command()
@commands.has_role('Host')
async def ready(ctx, eid):
    """Only for hosts: Mentions next user in queue of <event_id>"""
    print(f"Ready command sent from server: {ctx.message.guild.name} by {ctx.message.author}")
    sys.stdout.flush()
    if not check_events_server(ctx):
        await ctx.send("Sorry, I wasn't able to find any events")
    else:
        server_events = servers[ctx.guild.id]
        event_id = int(eid)
        if event_id not in server_events:
            await ctx.send(f"Sorry, I wasn't able to find any event with ID: {event_id}")
        elif ctx.author != server_events[event_id].host:
            await ctx.send("You are not the host for this event. Only the host can run this command for this event.")
        else:
            await ctx.send(f"{server_events[event_id].currently_served().mention}, "
                           f"{server_events[event_id].host.display_name} is ready for you!")


@client.command()
async def rename(ctx, eid, ind, *, new_question):
    """Renames question at <ind> to <new_question>"""
    print(f"Rename command sent from server: {ctx.message.guild.name} by {ctx.message.author}")
    sys.stdout.flush()
    if not check_events_server(ctx):
        await ctx.send("Sorry, I wasn't able to find any events")
    else:
        server_events = servers[ctx.guild.id]
        event_id = int(eid)
        question_index = int(ind)
        if event_id not in server_events:
            await ctx.send(f"Sorry, I wasn't able to find any event with ID: {event_id}")
        else:
            current = server_events[event_id].get_question_at(int(question_index) - 1)
            if current.author != ctx.author:
                await ctx.send("You can only rename a topic that you entered.")
            else:
                current.topic = new_question
                await ctx.send("The topic was renamed")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(f"Error sent from server: {ctx.message.guild.name} by {ctx.message.author}")
        sys.stdout.flush()


load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

client.run(ACCESS_TOKEN)
