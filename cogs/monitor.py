from datetime import timedelta, datetime
import requests
import discord
from discord.ext import tasks, commands
from utils import config


class Monitor(commands.Cog):
    """Cog for monitoring server uptime and sending notifications"""

    currently_down = {}
    last_notification = {}
    known_servers = set()

    def __init__(self, bot):
        self.bot = bot
        self.monitor_uptime.start()
        print("Monitor cog initialized and monitoring task started")

    def cog_unload(self):
        self.monitor_uptime.cancel()
        print("Monitor cog unloaded and monitoring task stopped")

    @staticmethod
    def check_status(url):
        """
        Check if a server is up by making a GET request

        Args:
            url (str): URL to check

        Returns:
            str or None: "up" if server returns 200, "timeout" on connection error, "error" on non-200 response
        """
        print(f"Checking status for: {url}")
        try:
            response = requests.get(url=f"https://{url}/", timeout=5)
            if response.status_code == 200:
                print(f"  Result: UP (200)")
                return "up"
            else:
                print(f"  Result: ERROR ({response.status_code})")
                return "error"
        except requests.exceptions.RequestException as e:
            print(f"  Result: TIMEOUT or ERROR ({str(e)})")
            return "timeout"

    async def notify_down(self, name, address, channel, reason, force=False):
        """
        Send notification that a server is down

        Args:
            name (str): Server name
            address (str): Server address
            channel (discord.TextChannel): Channel to send notification to
            reason (str): Reason for downtime
            force (bool): Force notification even if recently sent
        """
        current_time = datetime.now()
        notify = False

        if address not in self.currently_down:
            self.currently_down[address] = 0
            self.last_notification[address] = current_time
            notify = True
            print(f"Notifying NEW DOWN: {name} ({address}) - {reason}")
        else:
            downtime_seconds = self.currently_down[address]
            time_since_last = (
                current_time - self.last_notification.get(address, datetime.min)).total_seconds()
            if time_since_last >= 120 or force:
                self.last_notification[address] = current_time
                notify = True
                print(
                    f"Notifying STILL DOWN: {name} ({address}) - {reason} (down for {downtime_seconds} seconds)")
            else:
                print(
                    f"Skipping notification for {name} ({address}) - last notification was {time_since_last} seconds ago")

        if notify:
            embed = discord.Embed(
                title=f"**:red_circle: {name} is down!**",
                color=discord.Color.red()
            )
            embed.add_field(name="Address", value=address, inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            if self.currently_down[address] > 0:
                downtime = str(timedelta(seconds=self.currently_down[address]))
                embed.add_field(name="Downtime", value=downtime, inline=False)
                embed.description = f"Server has been down for {downtime}"

            embed.add_field(name="Timestamp", value=discord.utils.utcnow().strftime(
                "%Y-%m-%d %H:%M:%S UTC"), inline=False)

            try:
                await channel.send(embed=embed)
                print(f"  Sent DOWN notification for {address}")
                config_data = config.get_config()
                if 'role_to_mention' in config_data and config_data['role_to_mention'] != 0:
                    await channel.send(f"<@&{config_data['role_to_mention']}>", delete_after=3)
                    print(f"  Sent role mention")
            except Exception as e:
                print(f"  ERROR sending notification: {e}")
        interval = config.get_config()['secs_between_ping']
        self.currently_down[address] = self.currently_down.get(
            address, 0) + interval
        print(
            f"  Updated downtime for {address} to {self.currently_down[address]} seconds")

    async def notify_up(self, name, address, channel):
        """
        Send notification that a server is back up

        Args:
            name (str): Server name
            address (str): Server address
            channel (discord.TextChannel): Channel to send notification to
        """
        if address in self.currently_down:
            print(
                f"Notifying UP: {name} ({address}) after {self.currently_down[address]} seconds")

            embed = discord.Embed(
                title=f"**:green_circle: {name} is up!**",
                color=discord.Color.green()
            )
            embed.add_field(name="Address", value=address, inline=False)
            embed.add_field(name="Downtime", value=str(
                timedelta(seconds=self.currently_down[address])), inline=False)
            embed.add_field(name="Timestamp", value=discord.utils.utcnow().strftime(
                "%Y-%m-%d %H:%M:%S UTC"), inline=False)

            try:
                await channel.send(embed=embed)
                print(f"  Sent UP notification for {address}")
                config_data = config.get_config()
                if 'role_to_mention' in config_data and config_data['role_to_mention'] != 0:
                    await channel.send(f"<@&{config_data['role_to_mention']}>", delete_after=3)
                    print(f"  Sent role mention")

            except Exception as e:
                print(f"  ERROR sending notification: {e}")
            self.currently_down.pop(address, None)
            self.last_notification.pop(address, None)

    async def check_new_servers(self, channel):
        """Check if there are any new servers that should be immediately checked"""
        servers = config.get_servers()
        server_addresses = set(server['address']
                               for server in servers if 'address' in server)
        new_servers = server_addresses - self.known_servers
        if new_servers:
            print(f"Found {len(new_servers)} new servers to check immediately")

            for server in servers:
                address = server.get('address', '')
                if address in new_servers:
                    name = server.get('name', 'Unknown Server')
                    print(
                        f"Immediately checking new server: {name} ({address})")

                    status = self.check_status(address)

                    if status == "error":
                        await self.notify_down(name, address, channel, "Non-200 response", force=True)
                    elif status == "timeout":
                        await self.notify_down(name, address, channel, "Request timed out", force=True)
                    else:
                        print(f"  New server {name} ({address}) is up")
                        embed = discord.Embed(
                            title=f"**:green_circle: {name} added to monitoring**",
                            description="Server is currently up and being monitored",
                            color=discord.Color.green()
                        )
                        embed.add_field(
                            name="Address", value=address, inline=False)
                        embed.add_field(name="Timestamp", value=discord.utils.utcnow().strftime(
                            "%Y-%m-%d %H:%M:%S UTC"), inline=False)

                        try:
                            await channel.send(embed=embed)
                            print(
                                f"  Sent initial UP notification for new server {address}")
                        except Exception as e:
                            print(f"  ERROR sending notification: {e}")
        self.known_servers = server_addresses

    @tasks.loop(seconds=30)
    async def monitor_uptime(self):
        """Periodically check server status and send notifications"""
        print("\n--- Starting monitoring cycle ---")
        await self.bot.wait_until_ready()
        config_data = config.get_config()
        servers = config.get_servers()
        new_interval = config_data.get('secs_between_ping', 30)
        if self.monitor_uptime.seconds != new_interval:
            self.monitor_uptime.change_interval(seconds=new_interval)
            print(f"Updated check interval to {new_interval} seconds")
        channel_id = config_data.get('notification_channel', 0)
        channel = self.bot.get_channel(channel_id)

        if not channel:
            print(
                f"WARNING: Could not find notification channel with ID {channel_id}")
            return

        print(f"Using notification channel: #{channel.name} ({channel.id})")
        print(f"Monitoring {len(servers)} servers")
        await self.check_new_servers(channel)

        for server in servers:
            name = server.get('name', 'Unknown Server')
            address = server.get('address', '')

            print(f"Checking server: {name} ({address})")

            if not address:
                print(f"  WARNING: Server {name} has no address, skipping")
                continue

            status = self.check_status(address)

            if status == "error":
                await self.notify_down(name, address, channel, "Non-200 response")
            elif status == "timeout":
                await self.notify_down(name, address, channel, "Request timed out")
            else:
                if address in self.currently_down:
                    await self.notify_up(name, address, channel)
                else:
                    print(f"  {name} ({address}) is still up")

        print("--- Monitoring cycle complete ---")

    @monitor_uptime.before_loop
    async def before_monitor(self):
        """Wait for the bot to be ready before starting the monitoring loop"""
        await self.bot.wait_until_ready()
        print("Bot is ready, starting monitor loop")

        servers = config.get_servers()
        self.known_servers = set(server.get('address', '')
                                 for server in servers if 'address' in server)
        print(f"Initialized monitoring for {len(self.known_servers)} servers")


async def setup(bot):
    """Set up the Monitor cog"""
    print("Setting up Monitor cog...")
    await bot.add_cog(Monitor(bot))
    print("Monitor cog setup complete!")
