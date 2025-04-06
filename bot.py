# # import os
# # import discord
# # from utils import config
# # from discord.ext import commands
# # from dotenv import load_dotenv

# # load_dotenv()

# # intents = discord.Intents.default()
# # intents.message_content = True

# # bot = commands.Bot(command_prefix='!', intents=intents, help_command=commands.DefaultHelpCommand(
# #     no_category="Commands"
# # ))

# # COGS = [
# #     'cogs.monitor',
# #     'cogs.ping',
# #     'cogs.status',
# #     'cogs.config'
# # ]


# # @bot.event
# # async def on_ready():
# #     """Called when the bot is ready"""
# #     print(f"Logged in as {bot.user.name}")
# #     print(f"Bot ID: {bot.user.id}")
# #     print(f"Discord.py Version: {discord.__version__}")
# #     print("------")

# #     cfg = config.get_config()
# #     servers = config.get_servers()

# #     print(f"Monitoring {len(servers)} server(s)")
# #     print(f"Notification channel: {cfg['notification_channel']}")
# #     print(f"Check interval: {cfg['secs_between_ping']} seconds")
# #     print("------")

# #     activity = discord.Activity(
# #         type=discord.ActivityType.watching,
# #         name=f"{len(servers)} server(s)"
# #     )
# #     await bot.change_presence(activity=activity)


# # @bot.command()
# # @commands.has_permissions(administrator=True)
# # async def reload(ctx):
# #     """Reload all cogs and configuration"""
# #     for cog in COGS:
# #         try:
# #             await bot.reload_extension(cog)
# #         except commands.ExtensionNotLoaded:
# #             await bot.load_extension(cog)

# #     await ctx.send("✅ All monitoring cogs have been reloaded")


# # def load_cogs():
# #     """Load all cogs"""
# #     for cog in COGS:
# #         try:
# #             bot.load_extension(cog)
# #             print(f"Loaded cog: {cog}")
# #         except Exception as e:
# #             print(f"Failed to load cog {cog}: {e}")


# # def main():
# #     """Main entry point"""
# #     os.makedirs('cogs', exist_ok=True)
# #     os.makedirs('utils', exist_ok=True)

# #     config.get_config()
# #     config.get_servers()

# #     load_cogs()

# #     token = os.environ.get('DISCORD_TOKEN')
# #     if not token:
# #         print("ERROR: No Discord token found in environment variables")
# #         print("Please set the DISCORD_TOKEN environment variable")
# #         print("Example: export DISCORD_TOKEN=your_token_here (Linux/macOS)")
# #         print("         set DISCORD_TOKEN=your_token_here (Windows CMD)")
# #         print("         $env:DISCORD_TOKEN=\"your_token_here\" (Windows PowerShell)")
# #         print("\nAlternatively, create a .env file in the same directory with:")
# #         print("DISCORD_TOKEN=your_token_here")
# #         exit(1)

# #     bot.run(token)


# # if __name__ == "__main__":
# #     main()

# import os
# import discord
# from discord.ext import commands
# from utils import config
# from dotenv import load_dotenv

# # Load environment variables from .env file (if present)
# load_dotenv()

# # Set up intents
# intents = discord.Intents.default()
# intents.message_content = True  # This is crucial for command processing
# intents.guilds = True
# intents.guild_messages = True

# # Create bot instance
# bot = commands.Bot(
#     command_prefix='!',
#     intents=intents,
#     help_command=commands.DefaultHelpCommand(no_category="Commands"),
#     case_insensitive=True  # Makes commands case-insensitive
# )

# # List of cogs to load
# COGS = [
#     'cogs.monitor',
#     'cogs.ping',
#     'cogs.status',
#     'cogs.config'
# ]


# @bot.event
# async def on_ready():
#     """Called when the bot is ready"""
#     print(f"\n{'='*50}")
#     print(f"Logged in as {bot.user.name}")
#     print(f"Bot ID: {bot.user.id}")
#     print(f"Discord.py Version: {discord.__version__}")
#     print(f"{'='*50}\n")

#     # Log all available commands
#     print("Available commands:")
#     for command in bot.commands:
#         print(f"  !{command.name}: {command.brief or 'No description'}")
#     print('\n')

#     # Load configuration
#     cfg = config.get_config()
#     servers = config.get_servers()

#     print(f"Monitoring {len(servers)} server(s)")
#     print(f"Notification channel: {cfg['notification_channel']}")
#     print(f"Check interval: {cfg['secs_between_ping']} seconds")
#     print("------")

#     # Set bot status
#     activity = discord.Activity(
#         type=discord.ActivityType.watching,
#         name=f"{len(servers)} server(s)"
#     )
#     await bot.change_presence(activity=activity)


# @bot.event
# async def on_message(message):
#     """Log message processing for debugging"""
#     # Don't respond to our own messages
#     if message.author == bot.user:
#         return

#     # Log the message for debugging
#     if message.content and message.content.startswith('!'):
#         print(f"Command received: {message.content} from {message.author}")

#     # This is required to process commands
#     await bot.process_commands(message)


# @bot.event
# async def on_command_error(ctx, error):
#     """Handle command errors"""
#     if isinstance(error, commands.errors.CommandNotFound):
#         return  # Silently ignore unknown commands

#     if isinstance(error, commands.errors.MissingRequiredArgument):
#         await ctx.send(f"Missing required argument: {error.param.name}")
#         return

#     if isinstance(error, commands.errors.MissingPermissions):
#         await ctx.send("You don't have permission to use this command.")
#         return

#     # Log all other errors
#     print(f"Command error: {error}")
#     await ctx.send(f"Error: {error}")


# @bot.command(name="hello")
# async def hello(ctx):
#     """Simple command to test if the bot is responsive"""
#     await ctx.send(f"Hello {ctx.author.mention}! I'm online and ready.")


# @bot.command()
# @commands.has_permissions(administrator=True)
# async def reload(ctx):
#     """Reload all cogs and configuration"""
#     reloaded = []
#     failed = []

#     for cog in COGS:
#         try:
#             await bot.reload_extension(cog)
#             reloaded.append(cog)
#         except commands.ExtensionNotLoaded:
#             try:
#                 await bot.load_extension(cog)
#                 reloaded.append(cog)
#             except Exception as e:
#                 print(f"Failed to load cog {cog}: {e}")
#                 failed.append(f"{cog}: {e}")
#         except Exception as e:
#             print(f"Failed to reload cog {cog}: {e}")
#             failed.append(f"{cog}: {e}")

#     response = "✅ Reloaded cogs: " + ", ".join(reloaded)
#     if failed:
#         response += "\n❌ Failed to reload: " + ", ".join(failed)

#     await ctx.send(response)


# def load_cogs():
#     """Load all cogs"""
#     loaded = []
#     failed = []

#     for cog in COGS:
#         try:
#             bot.load_extension(cog)
#             loaded.append(cog)
#             print(f"Loaded cog: {cog}")
#         except Exception as e:
#             failed.append(f"{cog}: {e}")
#             print(f"Failed to load cog {cog}: {e}")

#     if loaded:
#         print(f"Successfully loaded {len(loaded)} cogs: {', '.join(loaded)}")
#     if failed:
#         print(f"Failed to load {len(failed)} cogs:")
#         for failure in failed:
#             print(f"  - {failure}")


# def main():
#     """Main entry point"""
#     # Create necessary directories
#     os.makedirs('cogs', exist_ok=True)
#     os.makedirs('utils', exist_ok=True)

#     # Ensure config files exist
#     config.get_config()
#     config.get_servers()

#     # Load cogs
#     load_cogs()

#     # Get token from environment
#     token = os.environ.get('DISCORD_TOKEN')
#     if not token:
#         print("ERROR: No Discord token found in environment variables")
#         print("Please set the DISCORD_TOKEN environment variable")
#         print("Example: export DISCORD_TOKEN=your_token_here (Linux/macOS)")
#         print("         set DISCORD_TOKEN=your_token_here (Windows CMD)")
#         print("         $env:DISCORD_TOKEN=\"your_token_here\" (Windows PowerShell)")
#         print("\nAlternatively, create a .env file in the same directory with:")
#         print("DISCORD_TOKEN=your_token_here")
#         exit(1)

#     # Start the bot
#     print("Starting bot...")
#     bot.run(token)


# if __name__ == "__main__":
#     main()


import os
import sys
import traceback
import discord
from discord.ext import commands
from utils import config
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Required for command processing
intents.guilds = True
intents.guild_messages = True

# Create bot instance
bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    help_command=commands.DefaultHelpCommand(no_category="Commands"),
    case_insensitive=True
)

# List of cogs to load
COGS = [
    'cogs.monitor',
    'cogs.ping',
    'cogs.status',
    'cogs.config'
]


@bot.event
async def on_ready():
    """Called when the bot is ready"""
    print(f"\n{'='*50}")
    print(f"Logged in as {bot.user.name}")
    print(f"Bot ID: {bot.user.id}")
    print(f"Discord.py Version: {discord.__version__}")
    print(f"{'='*50}\n")

    # Log all available commands
    print("Available commands:")
    for command in bot.commands:
        print(f"  !{command.name}: {command.brief or 'No description'}")
    print('\n')

    # Load configuration
    cfg = config.get_config()
    servers = config.get_servers()

    print(f"Monitoring {len(servers)} server(s)")
    print(f"Notification channel: {cfg['notification_channel']}")
    print(f"Check interval: {cfg['secs_between_ping']} seconds")
    print("------")

    # Set bot status
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=f"{len(servers)} server(s)"
    )
    await bot.change_presence(activity=activity)


@bot.event
async def on_message(message):
    """Log message processing for debugging"""
    # Don't respond to our own messages
    if message.author == bot.user:
        return

    # Log the message for debugging
    if message.content and message.content.startswith('!'):
        print(f"Command received: {message.content} from {message.author}")

    # This is required to process commands
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send(f"Command not found: {ctx.message.content}")
        return

    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param.name}")
        return

    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
        return

    # Log all other errors
    print(f"Command error: {error}")
    print("Full traceback:")
    traceback.print_exception(type(error), error, error.__traceback__)
    await ctx.send(f"Error: {error}")


@bot.command(name="hello")
async def hello(ctx):
    """Simple command to test if the bot is responsive"""
    await ctx.send(f"Hello {ctx.author.mention}! I'm online and ready.")


@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx):
    """Reload all cogs and configuration"""
    reloaded = []
    failed = []

    for cog in COGS:
        try:
            await bot.reload_extension(cog)
            reloaded.append(cog)
        except commands.ExtensionNotLoaded:
            try:
                await bot.load_extension(cog)
                reloaded.append(cog)
            except Exception as e:
                print(f"Failed to load cog {cog}: {e}")
                failed.append(f"{cog}: {e}")
        except Exception as e:
            print(f"Failed to reload cog {cog}: {e}")
            failed.append(f"{cog}: {e}")

    response = "✅ Reloaded cogs: " + ", ".join(reloaded)
    if failed:
        response += "\n❌ Failed to reload: " + ", ".join(failed)

    await ctx.send(response)


@bot.command()
@commands.has_permissions(administrator=True)
async def loadconfig(ctx):
    """Manually load the config cog"""
    try:
        # First try to import the module directly to check for syntax errors
        print("Attempting to import config cog...")
        from cogs.config import Config
        print("Config cog imported successfully!")

        # Now try to load it as an extension
        try:
            await bot.unload_extension('cogs.config')
        except:
            pass  # It's okay if it wasn't loaded

        await bot.load_extension('cogs.config')
        await ctx.send("✅ Config cog loaded!")

        # Show available commands after loading
        commands_list = [f"!{cmd.name}" for cmd in bot.commands]
        await ctx.send(f"Available commands: {', '.join(commands_list)}")

    except Exception as e:
        error_msg = f"❌ Error loading config cog: {e}"
        print(error_msg)
        traceback.print_exc()
        await ctx.send(error_msg)


@bot.command()
async def setup_defaults(ctx):
    """Set up default configuration based on the current channel"""
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("⚠️ You need administrator permissions to use this command")
        return

    # Get the bot's own role to use as a default role to mention
    bot_role = None
    for role in ctx.guild.roles:
        if role.name == bot.user.name:
            bot_role = role
            break

    # If no bot role, use the default role (@everyone)
    if not bot_role:
        bot_role = ctx.guild.default_role

    # Set up default configuration
    cfg = config.get_config()
    cfg['notification_channel'] = ctx.channel.id
    cfg['role_to_mention'] = bot_role.id
    cfg['secs_between_ping'] = 60
    config.save_config(cfg)

    # Add a default server to monitor
    servers = config.get_servers()
    if not servers:
        servers.append({
            'name': 'Example Website',
            'address': 'example.com'
        })
        config.save_servers(servers)

    await ctx.send(f"✅ Default configuration set up:\n" +
                   f"• Notification channel: {ctx.channel.mention}\n" +
                   f"• Role to mention: {bot_role.mention}\n" +
                   f"• Check interval: 60 seconds")


def load_cogs():
    """Load all cogs"""
    loaded = []
    failed = []

    for cog in COGS:
        try:
            bot.load_extension(cog)
            loaded.append(cog)
            print(f"Loaded cog: {cog}")
        except Exception as e:
            failed.append(f"{cog}: {e}")
            print(f"Failed to load cog {cog}: {e}")
            traceback.print_exc()

    if loaded:
        print(f"Successfully loaded {len(loaded)} cogs: {', '.join(loaded)}")
    if failed:
        print(f"Failed to load {len(failed)} cogs:")
        for failure in failed:
            print(f"  - {failure}")


def test_cog_import():
    """Test importing each cog directly to check for syntax errors"""
    for cog in COGS:
        try:
            module_path = cog.split('.')
            if len(module_path) == 2:
                module_name, class_name = module_path
                exec(f"from {module_name} import {class_name}")
                print(f"✅ Successfully imported {cog}")
        except Exception as e:
            print(f"❌ Error importing {cog}: {e}")
            traceback.print_exc()


def main():
    """Main entry point"""
    # Create necessary directories
    os.makedirs('cogs', exist_ok=True)
    os.makedirs('utils', exist_ok=True)

    # Test imports first
    print("Testing cog imports...")
    test_cog_import()

    # Ensure config files exist
    config.get_config()
    config.get_servers()

    # Load cogs
    load_cogs()

    # Get token from environment
    token = os.environ.get('DISCORD_TOKEN')
    if not token:
        print("ERROR: No Discord token found in environment variables")
        print("Please set the DISCORD_TOKEN environment variable")
        print("Example: export DISCORD_TOKEN=your_token_here (Linux/macOS)")
        print("         set DISCORD_TOKEN=your_token_here (Windows CMD)")
        print("         $env:DISCORD_TOKEN=\"your_token_here\" (Windows PowerShell)")
        print("\nAlternatively, create a .env file in the same directory with:")
        print("DISCORD_TOKEN=your_token_here")
        exit(1)

    # Start the bot
    print("Starting bot...")
    bot.run(token)


if __name__ == "__main__":
    main()
