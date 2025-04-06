from datetime import timedelta
import discord
from discord.ext import commands
from utils import config
from cogs.monitor import Monitor


class Status(commands.Cog):
    """Cog for checking and displaying server status"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Checks status of monitored servers")
    async def status(self, ctx):
        """
        Display the current status of all monitored servers

        Args:
            ctx (commands.Context): Command context
        """
        servers = config.get_servers()

        # If no servers configured
        if not servers:
            await ctx.send("No servers are currently being monitored.")
            return

        # Create embed with appropriate color (red if any server is down, green otherwise)
        color = discord.Color.red() if Monitor.currently_down else discord.Color.green()
        embed = discord.Embed(
            title="**Server Status Monitor**",
            description=f"Monitoring {len(servers)} server(s)",
            color=color
        )

        # Add status for each server
        for server in servers:
            address = server['address']
            name = server['name']

            if address in Monitor.currently_down:
                downtime = str(
                    timedelta(seconds=Monitor.currently_down[address]))
                value = f":red_circle: Down for {downtime}"
            else:
                value = f":green_circle: Online"

            embed.add_field(
                name=f"{name} ({address})",
                value=value,
                inline=False
            )

        # Add footer with refresh info
        config_data = config.get_config()
        refresh_interval = config_data.get('secs_between_ping', 60)
        embed.set_footer(
            text=f"Status refreshed every {refresh_interval} seconds")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Status(bot))