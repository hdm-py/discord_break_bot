# Break Bot for Discord

## Overview
Break Bot is a Discord bot designed to help users manage breaks in a server. Admins can set, modify, and end breaks, while the bot notifies users of active break times and their scheduled end. The bot can also send reminders 5 minutes before a break ends.

## Features
- **Set break time**: Admins can schedule a break using the `!break HH:MM` command.
- **Change break time**: Admins can modify the break time with `!change_break HH:MM`.
- **End break manually**: Admins can end the break early using `!end_break`.
- **Notify users**: Users can check the break end time using `!rast`.
- **Reminders**: Automatically sends a reminder 5 minutes before the break ends.

## Prerequisites
- Python 3.8+
- `discord.py` library
- `.env` file containing the bot's token

---

## Setup Instructions

### 1. Clone the Repository
Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/discord_bot_break.git
cd discord_bot_break
```

### 2. Set Up a Virtual Environment
It is recommended to create a virtual environment to manage dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
Ensure you have all the required Python packages by installing the dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Create `.env` File
Create a `.env` file in the root of your project with the following content:

```
DISCORD_TOKEN=your-discord-bot-token
```

Replace `your-discord-bot-token` with your bot's actual token.

### 5. Running the Bot
Run the bot after setting up the `.env` file:

```bash
python main.py
```

---

## Commands

### 1. `!break HH:MM`
Admins set the break time.
- **Example**: `!break 13:30`
- **Response**: "Break time is set to 13:30."

### 2. `!change_break HH:MM`
Admins modify the break time.
- **Example**: `!change_break 14:00`
- **Response**: "Break time has been changed to 14:00."

### 3. `!end_break`
Admins manually end the break.
- **Response**: "The break has been ended."

### 4. `!rast`
Users check the current break end time.
- **Example**: `!rast`
- **Response**: "The break ends at HH:MM." or "No break is currently set."

---

## Example Usage

**Admin**: `!break 13:30`  
**Bot**: "Break time is set to 13:30."

**Admin**: `!change_break 14:00`  
**Bot**: "Break time has been changed to 14:00."

**User**: `!rast`  
**Bot**: "The break ends at 13:30."

**Admin**: `!end_break`  
**Bot**: "The break has been ended."

---

## Notes
- Break times must be provided in a 24-hour format (HH:MM).
- The bot sends reminders 5 minutes before a break ends.
- Users can actively check break status using the `!rast` command.
- Only admins can use `!break`, `!change_break`, and `!end_break` commands.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

