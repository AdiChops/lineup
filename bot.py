import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

@client.event()
async def on_ready():
    print('Bot is ready.')

client.run('ODA1MTIwMTc4ODAyMzkzMTA4.YBWQmQ.HynCQfH1FcaRR-ah6UycFOd7sSs')
