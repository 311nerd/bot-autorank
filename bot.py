import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv, find_dotenv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="&", intents=intents, help_command=None)

load_dotenv(find_dotenv())

TAG=os.environ.get("TAG")
BOT_TOKEN=os.environ.get("BOT_TOKEN")
ROLE_AUTORANK=os.environ.get("ROLE_AUTORANK")
MEMBER_ROLE=os.environ.get("MEMBER_ROLE")

@bot.event
async def on_ready():
    print(f'{bot.user} est connecté!')
    bot.status = discord.Status.dnd
    activity = discord.Activity(type=discord.ActivityType.streaming,url = "https://twitch.tv/discord", name="PING=RANK")
    await bot.change_presence(activity=activity)

@bot.event
async def on_message(message):
    member = message.author
    if bot.user.mentioned_in(message):
        with open('blacklist.json', 'r') as f:
            blacklist = json.load(f)
            if str(member.id) in blacklist['blacklist']:
                await message.channel.send(f"{member.mention} vous êtes blacklisté, vous ne pouvez donc pas être rank.")
                return
        if TAG in member.display_name:
            role = discord.utils.get(member.guild.roles, id=int(ROLE_AUTORANK))
        else:
            await message.channel.send(f'{member.mention}, vous devez avoir le tag pour être rank !')
        if role not in member.roles:
            await member.add_roles(role)
            await message.channel.send(f'{member.mention}, vous avez été rank **{role.name}** !')
        else:
            await message.channel.send(f'{member.mention}, vous avez déjà le rank **{role.name}**.')
    if TAG in member.display_name:
        return
    else:
            role2 = discord.utils.get(member.guild.roles, id=int(MEMBER_ROLE))
            await member.edit(roles=[])
            await member.add_roles(role2)
            await message.channel.send(f"{member.mention}, vous avez été derank car vous n'avez plus le tag !")

@bot.command(alias="whitelist")
async def wl(ctx, user: discord.Member):
    with open('whitelist.json', 'r') as f:
        whitelist = json.load(f)
    if str(user.id) in whitelist['whitelist']:
        await ctx.send(f"{user.mention} est déjà whitelisté.")
    else:
        whitelist['whitelist'].append(str(user.id))
        with open('whitelist.json', 'w') as f:
            json.dump(whitelist, f)
        await ctx.send(f"{user.mention} a été whitelisté.")

@bot.command(alias="blacklist")
async def bl(ctx, user: discord.Member):
    with open('blacklist.json', 'r') as f:
        blacklist = json.load(f)
    if str(user.id) in blacklist['blacklist']:
        await ctx.send(f"{user.mention} est déjà blacklisté.")
    else:
        blacklist['blacklist'].append(str(user.id))
        with open('blacklist.json', 'w') as f:
            json.dump(blacklist, f)
        await ctx.send(f"{user.mention} a été blacklisté.")

bot.run(BOT_TOKEN)