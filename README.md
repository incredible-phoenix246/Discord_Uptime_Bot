# Discord Server Uptime Monitor

A Discord bot that monitors the uptime of web servers and sends notifications when they go down or come back online.

## Features

- **Server Monitoring**: Periodically checks the status of multiple web servers
- **Real-time Notifications**: Sends alerts when servers go down or come back up
- **Role Mentions**: Mentions a specific role in notifications to alert the right team
- **Status Command**: Quickly check the current status of all monitored servers
- **Ping Command**: Test the connectivity to specific addresses
- **Configuration System**: Easy-to-use commands to configure the bot

## Installation

### Prerequisites

- Python 3.8 or higher
- A Discord account and bot token
- Server with internet access

### Setup Steps

1. **Clone the repository**:

   ```bash
   git clone [https://github.com/yourusername/discord-website-uptime.git](https://github.com/incredible-phoenix246/Discord_Uptime_Bot.git)
   cd Discord_Uptime_Bot
   ```

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Discord bot token**:

   Create a `.env` file in the project root:

   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   ```

   Alternatively, set it as an environment variable:

   ```bash
   # Linux/macOS
   export DISCORD_TOKEN=your_discord_bot_token_here

   # Windows Command Prompt
   set DISCORD_TOKEN=your_discord_bot_token_here

   # Windows PowerShell
   $env:DISCORD_TOKEN="your_discord_bot_token_here"
   ```

5. **Invite the bot to your server**:

   - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
   - Select your application
   - Go to the OAuth2 > URL Generator tab
   - Select the `bot` and `applications.commands` scopes
   - Select the necessary permissions:
     - Read Messages/View Channels
     - Send Messages
     - Embed Links
     - Read Message History
     - Mention Everyone (if you want role mentions)
   - Open the generated URL and select your server

6. **Enable Required Intents**:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
   - Select your application
   - Go to the Bot tab
   - Under "Privileged Gateway Intents", enable:
     - Message Content Intent
     - Server Members Intent
     - Presence Intent (optional)

## Running the Bot

Start the bot with:

```bash
python3 bot.py
```

Once the bot is running and has joined your server, set up the initial configuration:

```
!setup_defaults
```

This will configure the notification channel to the current channel and set up basic settings.

## Configuration

### Basic Commands

- `!config` - Display current configuration
- `!status` - Show the current status of all monitored servers
- `!ping example.com` - Ping a specific server (1-10 pings)
- `!hello` - Test if the bot is responsive
- `!help` - Display available commands
- `!loadconfig` - Manually load the config cog (useful for debugging)
- `!setup_defaults` - Quickly set up the bot with default configuration

### Advanced Configuration

- `!config channel #channel-name` - Set the notification channel
- `!config role @role-name` - Set the role to mention in notifications
- `!config interval 60` - Set how often servers are checked (in seconds, minimum 30)
- `!config addserver "My Website" example.com` - Add a server to monitor
- `!config removeserver example.com` - Remove a server from monitoring
- `!config help` - Show configuration command help

## Project Structure

```
discord-website-uptime/
├── bot.py                 # Main bot file
├── requirements.txt       # Python dependencies
├── config.json            # Bot configuration
├── servers.json           # List of servers to monitor
├── .env                   # Environment variables (Discord token)
├── cogs/
│   ├── config.py          # Configuration commands
│   ├── monitor.py         # Server monitoring functionality
│   ├── ping.py            # Server ping command
│   └── status.py          # Status display command
└── utils/
    └── config.py          # Configuration file handling
```

## Troubleshooting

### Common Issues

- **Bot doesn't respond to commands**:

  - Ensure the bot has the necessary permissions in the channel
  - Check that you've enabled the Message Content Intent in the Discord Developer Portal
  - Verify the bot is online in your server

- **"Command not found" errors**:

  - Make sure you're using the correct prefix (default: `!`)
  - Check if the bot has successfully loaded all cogs (look at startup logs)

- **Cog loading errors**:

  - Ensure all cog files have an `async def setup(bot)` function, not `def setup(bot)`
  - Check for syntax errors in your Python files

- **Configuration not saving**:
  - Ensure the bot has write permissions in its directory
  - Check for any errors in the console output

## Customization

### Modifying Check Interval

The default check interval is 60 seconds. To change it:

```
!config interval 120  # Check every 2 minutes
```

Avoid setting intervals below 30 seconds to prevent rate limiting.

### Adding Custom Monitoring Logic

To add custom monitoring logic, modify the `check_status` method in `cogs/monitor.py`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper for Python
- [requests](https://requests.readthedocs.io/) - HTTP library for Python
- [ping3](https://github.com/kyan001/ping3) - Pure Python ICMP ping implementation
