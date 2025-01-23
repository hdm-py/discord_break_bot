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

# Global variable to store the break end time
break_end_time = None

# Global variable to store if a reminder has been sent
reminder_sent = False

async def break_reminder_task():
    """
    Background task to check and send a reminder 10 minutes before the break ends.
    """
    global break_end_time, reminder_sent
    while True:
        if break_end_time:
            current_time = datetime.now().time()
            # Calculate time difference in minutes
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
        else:
            reminder_sent = False
        await asyncio.sleep(60)  # Check every minute

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")
    print(f"Loaded commands: {[command.name for command in bot.commands]}")
    # Start the background task
    bot.loop.create_task(break_reminder_task())

@bot.command(name="break")
async def set_break(ctx, time: str):
    """
    Sets the break end time.
    Command format: !break HH:MM (24-hour format)
    """
    global break_end_time
    try:
        break_end_time = datetime.strptime(time, "%H:%M").time()
        await ctx.send(f"Break time is set to {time}.")
    except ValueError:
        await ctx.send("Please provide the time in HH:MM format, e.g., !break 13:30.")

@bot.command(name="change_break")
async def change_break(ctx, time: str):
    """
    Changes the break end time.
    Command format: !change_break HH:MM (24-hour format)
    """
    global break_end_time, reminder_sent
    try:
        break_end_time = datetime.strptime(time, "%H:%M").time()
        reminder_sent = False  # Reset reminder flag
        await ctx.send(f"Break time has been changed to {time}.")
    except ValueError:
        await ctx.send("Please provide the time in HH:MM format, e.g., !change_break 14:00.")

@bot.command(name="end_break")
async def end_break(ctx):
    """
    Ends the break manually.
    Command format: !end_break
    """
    global break_end_time
    break_end_time = None
    await ctx.send("The break has been ended.")

@bot.command(name="rast")
async def get_break_time(ctx):
    """
    Returns the current break end time if one is set.
    Command format: !rast
    """
    global break_end_time
    if break_end_time:
        await ctx.send(f"The break ends at {break_end_time.strftime('%H:%M')}.")
    else:
        await ctx.send("No break is currently set.")

@bot.event
async def on_message(message):
    """
    Handles messages and processes only bot commands.
    """
    # Skip bot's own messages
    if message.author.bot:
        return

    # Process bot commands only
    await bot.process_commands(message)

# Run the bot
bot.run(TOKEN)
