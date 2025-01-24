import discord
import asyncio
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Ensure message content intent is enabled
bot = commands.Bot(command_prefix="!", intents=intents)

# Global variables
break_end_time = None
reminder_sent = False
authorized_users = []  # Lista över användar-ID:n med admin-behörighet

def is_authorized(ctx):
    """
    Kontrollera om en användare är administratör eller finns i authorized_users.
    """
    return ctx.author.id in authorized_users or ctx.author.guild_permissions.administrator

async def break_reminder_task():
    """
    Kontrollera och skicka påminnelse 5 minuter innan rasten slutar och avsluta automatiskt rasten.
    """
    global break_end_time, reminder_sent
    while True:
        if break_end_time:
            current_time = datetime.now().time()
            time_left = (
                datetime.combine(datetime.today(), break_end_time) -
                datetime.combine(datetime.today(), current_time)
            ).total_seconds() / 60
            if time_left <= 5 and time_left > 0 and not reminder_sent:
                reminder_sent = True
                channel = discord.utils.get(bot.get_all_channels(), name="general")  # Replace with your channel name
                if channel:
                    await channel.send(
                        f"Reminder: The break will end in 5 minutes at {break_end_time.strftime('%H:%M')}!"
                    )
            if time_left <= 0:
                break_end_time = None
                reminder_sent = False
                channel = discord.utils.get(bot.get_all_channels(), name="general")
                if channel:
                    await channel.send("The break has ended.")
        else:
            reminder_sent = False
        await asyncio.sleep(60)

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")
    print(f"Loaded commands: {[command.name for command in bot.commands]}")
    bot.loop.create_task(break_reminder_task())

@bot.command(name="break")
async def set_break(ctx, time: str):
    """
    Ställ in rastens sluttid. Behörighet krävs.
    """
    if not is_authorized(ctx):
        await ctx.send("Du har inte behörighet att använda detta kommando.")
        return

    global break_end_time
    try:
        break_end_time = datetime.strptime(time, "%H:%M").time()
        await ctx.send(f"Break time is set to {time}.")
    except ValueError:
        await ctx.send("Please provide the time in HH:MM format, e.g., !break 13:30.")

@bot.command(name="change_break")
async def change_break(ctx, time: str):
    """
    Ändra rastens sluttid. Behörighet krävs.
    """
    if not is_authorized(ctx):
        await ctx.send("Du har inte behörighet att använda detta kommando.")
        return

    global break_end_time, reminder_sent
    try:
        break_end_time = datetime.strptime(time, "%H:%M").time()
        reminder_sent = False
        await ctx.send(f"Break time has been changed to {time}.")
    except ValueError:
        await ctx.send("Please provide the time in HH:MM format, e.g., !change_break 14:00.")

@bot.command(name="end_break")
async def end_break(ctx):
    """
    Avsluta rasten manuellt. Behörighet krävs.
    """
    if not is_authorized(ctx):
        await ctx.send("Du har inte behörighet att använda detta kommando.")
        return

    global break_end_time
    break_end_time = None
    await ctx.send("The break has been ended.")

@bot.command(name="rast")
async def get_break_time(ctx):
    """
    Visa rastens sluttid.
    """
    global break_end_time
    if break_end_time:
        await ctx.send(f"The break ends at {break_end_time.strftime('%H:%M')}.")
    else:
        await ctx.send("No break is currently set.")

@bot.command(name="add_permission")
@commands.has_permissions(administrator=True)
async def add_permission(ctx, user: discord.User):
    """
    Lägg till en användare i listan över auktoriserade användare.
    """
    if user.id not in authorized_users:
        authorized_users.append(user.id)
        await ctx.send(f"{user.mention} har fått behörighet att använda admin-kommandon.")
    else:
        await ctx.send(f"{user.mention} har redan behörighet.")

@bot.command(name="remove_permission")
@commands.has_permissions(administrator=True)
async def remove_permission(ctx, user: discord.User):
    """
    Ta bort en användare från listan över auktoriserade användare.
    """
    if user.id in authorized_users:
        authorized_users.remove(user.id)
        await ctx.send(f"{user.mention} har fått sin behörighet borttagen.")
    else:
        await ctx.send(f"{user.mention} har inte behörighet.")

@bot.command(name="show_permissions")
@commands.has_permissions(administrator=True)
async def show_permissions(ctx):
    """
    Visa en lista över alla användare med särskild behörighet.
    """
    if authorized_users:
        users = [f"<@{user_id}>" for user_id in authorized_users]
        await ctx.send(f"Användare med behörighet: {', '.join(users)}")
    else:
        await ctx.send("Inga extra användare har behörighet.")

@bot.event
async def on_command_error(ctx, error):
    """
    Hanterar fel för kommandon, inklusive saknade behörigheter.
    """
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")
    else:
        raise error

bot.run(TOKEN)