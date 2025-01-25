# Discord Bot Documentation

## Overview
This bot is designed to manage breaks in a Discord server. Administrators or authorized users can set, modify, and monitor break times. The bot will also send reminders 5 minutes before a break ends and announce when the break is over.

---

## Features
1. **Set Break Time**: Define when the break will end.
2. **Change Break Time**: Modify the existing break end time.
3. **End Break Manually**: End the current break before the scheduled time.
4. **Break Time Status**: Display the current break end time.
5. **Reminders**: Notify the server 5 minutes before a break ends.
6. **User Permissions**: Grant or revoke admin-like permissions for bot commands.

---

## Commands

### General Commands

#### `!break_time <HH:MM>`
- **Description**: Set the break end time.
- **Permissions**: Admin or authorized users.
- **Example**: `!break_time 13:30`

#### `!change_break <HH:MM>`
- **Description**: Change the existing break end time.
- **Permissions**: Admin or authorized users.
- **Example**: `!change_break 14:00`

#### `!end_break`
- **Description**: Manually end the current break.
- **Permissions**: Admin or authorized users.
- **Example**: `!end_break`

#### `!break`
- **Description**: Display the current break end time.
- **Permissions**: All users.
- **Example**: `!break`

### User Management Commands

#### `!add_permission <@user>`
- **Description**: Grant a user permission to use admin commands.
- **Permissions**: Admin only.
- **Example**: `!add_permission @JohnDoe`

#### `!remove_permission <@user>`
- **Description**: Revoke a user's permission to use admin commands.
- **Permissions**: Admin only.
- **Example**: `!remove_permission @JohnDoe`

#### `!show_permissions`
- **Description**: List all users with special permissions.
- **Permissions**: Admin only.
- **Example**: `!show_permissions`

---

## Setup Instructions

### Prerequisites
1. Python 3.8 or higher.
2. Required Python packages:
   - `discord.py`
   - `python-dotenv`
3. A Discord bot token from the [Discord Developer Portal](https://discord.com/developers/applications).
4. A `.env` file containing your bot token:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   ```

### Virtual Environment
It is recommended to use a virtual environment to manage dependencies:
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - **Windows**: `venv\Scripts\activate`
   - **Mac/Linux**: `source venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Bot
1. Clone the repository or copy the bot's source code.
2. Navigate to the bot's directory in your terminal.
3. Ensure your `.env` file is properly set up with your bot token:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   ```
4. Run the bot:
   ```bash
   python main.py
   ```

---

## How It Works
1. The bot uses `discord.py` and listens for commands prefixed with `!`.
2. Authorized users can manage breaks, while regular users can only view break times.
3. The bot automatically sends reminders and announcements based on the set break time.

---

## Notes
1. Ensure the bot has the necessary permissions to read and send messages in your desired channel.
2. Replace `general` in the code with the name of the channel you want the bot to post reminders in.

---

## Troubleshooting
- **Bot not responding to commands:**
  1. Check that the bot is online.
  2. Verify the bot's permissions in your Discord server.
  3. Ensure the command prefix is correct (`!`).

- **Environment variables not loading:**
  1. Ensure `.env` is in the same directory as the bot.
  2. Verify the `DISCORD_TOKEN` key and value.

---

## License
This bot is provided under the MIT License. Feel free to modify and use it as needed.
