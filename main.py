import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

import json 
import asyncio
#loads my env file 

import json

def load_players():
    try:
        with open("Players.JSON", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_players(data):
    with open("Players.JSON", "w") as f:
        json.dump(data, f, indent=4)


load_dotenv()
token = os.getenv('DISCORD_TOKEN')

#for debugging 
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


# all intents u need bot to do. ADD MORE FOR OTHER USE
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# creates the bot, ! to talk to the bot 
bot = commands.Bot(command_prefix='!', intents=intents)



# events---------------------------------------------------  

# functions that respond to discord events without user typing sth

@bot.event
#async means other program can be still running at the same time while this function is runnign 
# on_ready is discord preexisting function 
async def on_ready():
    print(f"Discord bot is now active, {bot.user.name}")

@bot.event
async def on_member_join(member):
    # await is only in async, wait 
    #waiting on member.send
    await member.send(f"Welcome to the Henry's Server {member.name}")

#!hello woudl trigger this name of funciton is. command is when user ping the bot 
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")


@bot.command()
async def register(ctx):

    players = load_players()
    user_id = str(ctx.author.id)

    if user_id in players:
        await ctx.send("You're already registered!")
        return

    await ctx.send("Enter your username")
    
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    
    try:
        # Wait up to 30 seconds for a message from the same user in the same channel
        msg = await bot.wait_for("message", check=check, timeout=30)
        username = msg.content
        await ctx.send(f"Got it! Your username is **{username}**.")
    
    except asyncio.TimeoutError:
        # If user doesn’t reply in 30 seconds, this runs
        await ctx.send("Too slow, try again")
    
    username = msg.content

     # save player
    players[user_id] = {
        "username": username,
        "elo": 1000,  # default starting rating
        "rank": 0,
        "wins": 0,
        "loss": 0,

    }

    save_players(players)
    await ctx.send(f"✅ Registered **{username}** with ELO 1000!")

@bot.command() 
async def profile(ctx):
    players = load_players()
    user_id = str(ctx.author.id)
    

    if not(user_id in players):
        await ctx.send("You're not registered!")
        return

    # player is this one guy in the dictionary 
    player = players[user_id]
    #dictionary 
    username = player["username"]
    elo = player["elo"]
    wins = player["wins"]
    loss = player["loss"]

    await ctx.send(
    f"**🏓 Player Profile**\n"
    f"👤 Username: **{username}**\n"
    f"📈 ELO: **{elo}**\n"
    f"✅ Wins: **{wins}**\n"
    f"❌ Losses: **{loss}**"
)

@bot.command()
async def game(ctx, opponent: discord.Member, winner: str):
    
    players = load_players()  
    user_id = str(ctx.author.id)
    opp_id = str(opponent.id)

    if not(user_id in players):
        await ctx.send("You're not registered!")
        return
    if not(opp_id in players):
        await ctx.send("Opponent're not registered!")
        return
    

# make bot go live 
bot.run(token, log_handler=handler, log_level=logging.DEBUG)