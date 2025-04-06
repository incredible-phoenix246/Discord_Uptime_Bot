import discord
from discord.ext import commands
from utils import config


class Config(commands.Cog):
    """Cog for managing bot configuration"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        """Display or modify bot configuration"""
        if ctx.invoked_subcommand is None:
            await self.show_config(ctx)

    async def show_config(self, ctx):
        """Display current configuration"""
        cfg = config.get_config()
        servers = config.get_servers()

        embed = discord.Embed(
            title="Server Monitor Configuration",
            color=discord.Color.blue()
        )

        # Main settings
        channel = self.bot.get_channel(cfg['notification_channel'])
        channel_value = f"<#{cfg['notification_channel']}>" if channel else f"Invalid channel ID: {cfg['notification_channel']}"

        role = ctx.guild.get_role(
            cfg['role_to_mention']) if ctx.guild else None
        role_value = f"<@&{cfg['role_to_mention']}>" if role else f"Invalid role ID: {cfg['role_to_mention']}"

        embed.add_field(name="Notification Channel",
                        value=channel_value, inline=False)
        embed.add_field(name="Role to Mention", value=role_value, inline=False)
        embed.add_field(name="Check Interval",
                        value=f"{cfg['secs_between_ping']} seconds", inline=False)

        # Servers
        servers_text = ""
        for i, server in enumerate(servers, 1):
            servers_text += f"{i}. {server['name']} ({server['address']})\n"

        if servers_text:
            embed.add_field(
                name=f"Monitored Servers ({len(servers)})", value=servers_text, inline=False)
        else:
            embed.add_field(name="Monitored Servers",
                            value="No servers configured", inline=False)

        # Help footer
        embed.set_footer(text="Use !config help to see available commands")

        await ctx.send(embed=embed)

    @config.command()
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        """Set the notification channel"""
        cfg = config.get_config()
        cfg['notification_channel'] = channel.id
        config.save_config(cfg)

        await ctx.send(f"✅ Notification channel set to {channel.mention}")

    @config.command()
    @commands.has_permissions(administrator=True)
    async def role(self, ctx, role: discord.Role):
        """Set the role to mention"""
        cfg = config.get_config()
        cfg['role_to_mention'] = role.id
        config.save_config(cfg)

        await ctx.send(f"✅ Mention role set to {role.mention}")

    @config.command()
    @commands.has_permissions(administrator=True)
    async def interval(self, ctx, seconds: int):
        """Set the status check interval in seconds"""
        if seconds < 30:
            await ctx.send("⚠️ Interval must be at least 30 seconds to avoid rate limiting")
            return

        cfg = config.get_config()
        cfg['secs_between_ping'] = seconds
        config.save_config(cfg)

        await ctx.send(f"✅ Status check interval set to {seconds} seconds")

    @config.command()
    @commands.has_permissions(administrator=True)
    async def addserver(self, ctx, name: str, address: str):
        """Add a server to monitor"""
        servers = config.get_servers()

        # Check if server already exists
        for server in servers:
            if server['address'].lower() == address.lower():
                await ctx.send(f"⚠️ Server with address {address} already exists")
                return

        # Add new server
        servers.append({
            'name': name,
            'address': address
        })

        config.save_servers(servers)

        # Update bot activity
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(servers)} server(s)"
        )
        await self.bot.change_presence(activity=activity)

        await ctx.send(f"✅ Added server: {name} ({address})")

    @config.command()
    @commands.has_permissions(administrator=True)
    async def removeserver(self, ctx, address: str):
        """Remove a server from monitoring"""
        servers = config.get_servers()

        # Find server by address
        found = False
        for i, server in enumerate(servers):
            if server['address'].lower() == address.lower():
                del servers[i]
                found = True
                break

        if not found:
            await ctx.send(f"⚠️ No server found with address {address}")
            return

        config.save_servers(servers)

        # Update bot activity
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(servers)} server(s)"
        )
        await self.bot.change_presence(activity=activity)

        await ctx.send(f"✅ Removed server with address {address}")

    @config.command()
    @commands.has_permissions(administrator=True)
    async def help(self, ctx):
        """Show config command help"""
        commands_list = [
            ("!config", "Show current configuration"),
            ("!config channel #channel", "Set notification channel"),
            ("!config role @role", "Set role to mention"),
            ("!config interval <seconds>", "Set check interval (min 30s)"),
            ("!config addserver <name> <address>", "Add server to monitor"),
            ("!config removeserver <address>", "Remove server from monitoring")
        ]

        embed = discord.Embed(
            title="Server Monitor Configuration Commands",
            color=discord.Color.blue()
        )

        for cmd, desc in commands_list:
            embed.add_field(name=cmd, value=desc, inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Config(bot))
