import discord
from discord.commands import Option
from discord.ext import commands, tasks
from dotenv import load_dotenv
import datetime, time
import os

intents = discord.Intents.default()

status = discord.Status.idle
activity = discord.Activity(type=discord.ActivityType.watching, name="Over this server for")

bot = discord.Bot(
    intents=intents,
    debug_guilds=[1291029673425502248],
    status=status,
    activity=activity
)

@bot.event
async def on_ready():
    print(f"{bot.user} ist online")
    channel = await bot.fetch_channel(INPUT_LOGS_CHANNEL_ID)
    await channel.send(f"{bot.user} is online now")
    global startTime
    startTime = time.time()

@bot.slash_command(description ="take a look how Devno is doing")
async def apa_status(ctx):
    uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
    
    
    embed = discord.Embed(
        title=f"status of {bot.user}",
        description=f"Here you can view all stats of {bot.user}",
        color=discord.Color.blurple()
    
    )
    
    rel_time = discord.utils.format_dt(bot.user.created_at, "R")
    
    embed.add_field(name="ID", value=bot.user.id)
    embed.add_field(name="First release", value=rel_time, inline=False)
    embed.add_field(name="Uptime", value=uptime)
    
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    embed.set_footer(text="all available stats where displayed successfully.")
    
    await ctx.respond(embed=embed)

@bot.slash_command(description="kick a member")
async def kick(ctx, member: Option(discord.Member, "chose a member")):
    try:
        await member.kick()
    except discord.Fordbidden:
        await ctx.responde("i don't have the permissions to kick that member")
        return
    await ctx.respond(f"{member.mention} was kicked by {bot.user}!")

@bot.slash_command(description="ping some users to anoy them")
async def ping(ctx, user: Option(discord.Member, "pings the selected user.")):
    await ctx.respond(f"oh hello there {user.mention}!")
    
@bot.slash_command(description="let apa send a message for you.")
async def say(ctx, text: Option(str, "say:"), channel: Option(discord.TextChannel)):
    await channel.send(text)
    await ctx.respond("sended message successfully", ephemeral=True)
    
@bot.slash_command(description="show infos about a user", name="userinfo")
async def info(
    ctx,  
    user: Option(discord.Member, "input username", default=None)
):
    if user is None:
        user = ctx.author
        
    embed = discord.Embed(
        title=f"infos about {user.name}",
        description=f"here you can see all infos about {user.mention}",
        color=discord.Color.blue()
    )
    
    time = discord.utils.format_dt(user.created_at, "R")
    
    embed.add_field(name="Acount created", value=time, inline=False)
    embed.add_field(name="ID", value=user.id)
    
    embed.set_thumbnail(url=user.display_avatar.url)
    embed.set_footer(text="all infos displayd successfully :)")

    await ctx.respond(embed=embed)

if __name__ == "__main__":
    load_dotenv()
    bot.run(os.getenv("TOKEN"))
