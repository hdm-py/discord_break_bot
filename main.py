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
authorized_users = []  # List of user IDs with admin permissions

def is_authorized(ctx):
    """
    Check if a user is authorized to use admin commands.
    """
    return ctx.author.id in authorized_users or ctx.author.guild_permissions.administrator

async def break_reminder_task():
    """
    Check and send a reminder 5 minutes before the break ends and automatically end the break.
    """
    global break_end_time, reminder_sent
    while True:
        if break_end_time:
            current_time = datetime.now()
            break_time = datetime.combine(datetime.today(), break_end_time)
            time_left = (break_time - current_time).total_seconds()

            # Handle short breaks less than 5 minutes
            if 0 < time_left <= 300 and not reminder_sent:  # 300 seconds = 5 minutes
                reminder_sent = True
                minutes, seconds = divmod(int(time_left), 60)
                channel = discord.utils.get(bot.get_all_channels(), name="general")  # Replace with your channel name
                if channel:
                    await channel.send(
                        f"Reminder: The break will end in {minutes} minute(s) and {seconds} second(s) at {break_end_time.strftime('%H:%M')}!"
                    )

            # End the break when the time is up
            if time_left <= 0:
                break_end_time = None
                reminder_sent = False
                channel = discord.utils.get(bot.get_all_channels(), name="general")
                if channel:
                    await channel.send("The break has ended.")
        else:
            reminder_sent = False

        await asyncio.sleep(1)  # Check every second for higher accuracy



@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")
    print(f"Loaded commands: {[command.name for command in bot.commands]}")
    bot.loop.create_task(break_reminder_task())

@bot.command(name="break_time")
async def set_break(ctx, time: str):
    """
    Set the break end time. Admin permissions required.
    """
    if not is_authorized(ctx):
        await ctx.send("You do not have permission to use this command.")
        return

    global break_end_time
    try:
        break_end_time = datetime.strptime(time, "%H:%M").time()
        await ctx.send(f"Break time is set to {time}.")
    except ValueError:
        await ctx.send("Please provide the time in HH:MM format, e.g., !break_time 13:30.")

@bot.command(name="change_break")
async def change_break(ctx, time: str):
    """
    Change the break end time. Admin permissions required.
    """
    if not is_authorized(ctx):
        await ctx.send("You do not have permission to use this command.")
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
    End the break manually. Admin permissions required.
    """
    if not is_authorized(ctx):
        await ctx.send("You do not have permission to use this command.")
        return

    global break_end_time
    break_end_time = None
    await ctx.send("The break has been ended.")

@bot.command(name="break")
async def get_break_time(ctx):
    """
    Display the current break end time.
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
    Add a user to the list of authorized users.
    """
    if user.id not in authorized_users:
        authorized_users.append(user.id)
        await ctx.send(f"{user.mention} has been granted permission to use admin commands.")
    else:
        await ctx.send(f"{user.mention} already has permission.")

@bot.command(name="remove_permission")
@commands.has_permissions(administrator=True)
async def remove_permission(ctx, user: discord.User):
    """
    Remove a user from the list of authorized users.
    """
    if user.id in authorized_users:
        authorized_users.remove(user.id)
        await ctx.send(f"{user.mention}'s permissions have been revoked.")
    else:
        await ctx.send(f"{user.mention} does not have any permissions.")

@bot.command(name="show_permissions")
@commands.has_permissions(administrator=True)
async def show_permissions(ctx):
    """
    Display a list of all users with special permissions.
    """
    if authorized_users:
        users = [f"<@{user_id}>" for user_id in authorized_users]
        await ctx.send(f"Users with permissions: {', '.join(users)}")
    else:
        await ctx.send("No additional users have permissions.")

@bot.event
async def on_command_error(ctx, error):
    """
    Handle errors for commands, including missing permissions.
    """
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")
    else:
        raise error

bot.run(TOKEN)
