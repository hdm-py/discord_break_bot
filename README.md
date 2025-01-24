# Break Bot for Discord

## Overview
Break Bot is a Discord bot designed to help manage breaks in a server. Admins can set, modify, and end breaks, while the bot notifies users of active break times and their scheduled end. The bot also sends reminders 5 minutes before a break ends.

---

## Features

- **Set break time**: Admins can schedule a break using the `!break_time HH:MM` command.
- **Change break time**: Admins can modify the break time with `!change_break HH:MM`.
- **End break manually**: Admins can end the break early using `!end_break`.
- **Notify users**: Users can check the break end time using `!break`.
- **Reminders**: Automatically sends a reminder 5 minutes before the break ends.
- **Permission management**: Add or remove users who can use admin commands.

---

## Prerequisites

- Python 3.8 or higher
- `discord.py` library
- `.env` file containing the bot's token

---

## Setup Instructions

### 1. Clone the Repository
Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/discord_break_bot.git
cd discord_break_bot
2. Set Up a Virtual Environment
Create a virtual environment to manage dependencies:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
Install the required Python packages:

pip install -r requirements.txt
4. Create .env File
Create a .env file in the root of your project with the following content:

DISCORD_TOKEN=your-discord-bot-token
Replace your-discord-bot-token with your bot's actual token.

5. Running the Bot
Run the bot after setting up the .env file:

python main.py
Commands

Admin Commands
1. !break_time HH:MM

Sets the break end time.

Example: !break_time 13:30
Response: "Break time is set to 13:30."
2. !change_break HH:MM

Changes the break end time.

Example: !change_break 14:00
Response: "Break time has been changed to 14:00."
3. !end_break

Ends the break manually.

Response: "The break has been ended."
4. !add_permission @user

Grants a user permission to use admin commands.

Response: "@user has been granted permission."
5. !remove_permission @user

Removes a user’s permission to use admin commands.

Response: "@user's permission has been removed."
6. !show_permissions

Displays a list of users with admin permissions.

Response: "Authorized users: @user1, @user2."
User Commands
1. !break

Displays the current break end time.

Example: !break
Response: "The break ends at 13:30." or "No break is currently set."
Example Usage

Admin: !break_time 13:30
Bot: "Break time is set to 13:30."

Admin: !change_break 14:00
Bot: "Break time has been changed to 14:00."

User: !break
Bot: "The break ends at 14:00."

Admin: !end_break
Bot: "The break has been ended."

Admin: !add_permission @user
Bot: "@user has been granted permission."

Admin: !remove_permission @user
Bot: "@user's permission has been removed."

Notes

Break times must be provided in a 24-hour format (HH:MM).
The bot sends reminders 5 minutes before a break ends.
Users can actively check break status using the !break command.
Only admins or authorized users can set, modify, or end breaks.
License

This project is licensed under the MIT License. See the LICENSE file for details.