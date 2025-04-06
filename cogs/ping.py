import asyncio
from discord.ext import commands
from ping3 import ping as ping3_ping


class Ping(commands.Cog):
    """Cog for pinging servers via ICMP"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Pings an address - ping <address> [pings]")
    async def ping(self, ctx, address: str, pings: int = 1):
        """
        Ping a server and display response time

        Args:
            ctx (commands.Context): Command context
            address (str): Address to ping
            pings (int, optional): Number of pings to send. Defaults to 1.
        """
        # Validate input
        if pings < 1:
            await ctx.send("Number of pings must be at least 1")
            return

        if pings > 10:
            await ctx.send("Maximum number of pings is 10 to prevent abuse")
            return

        # Send initial message
        status_msg = await ctx.send(f"Pinging {address}...")

        results = []
        failed = 0

        # Perform pings
        for i in range(pings):
            result = ping3_ping(address, timeout=2, unit='ms')

            if result is False:
                await status_msg.edit(content=f"Could not ping {address} - unknown host.")
                return
            elif result is None:
                failed += 1
                results.append("Timed out")
            else:
                # Round to 2 decimal places
                latency = round(result, 2)
                results.append(f"{latency}ms")

            # Wait between pings to avoid flooding
            if i < pings - 1:
                await asyncio.sleep(1)

        # Format response message
        if failed == pings:
            response = f"Failed to reach {address} - all {pings} attempt(s) timed out."
        else:
            response = f"**Ping results for {address}:**\n"
            for i, result in enumerate(results, 1):
                response += f"Ping {i}: {result}\n"

            if failed > 0:
                response += f"\n{failed} out of {pings} packets lost ({failed/pings*100:.1f}% loss)"

        await status_msg.edit(content=response)


async def setup(bot):
    await bot.add_cog(Ping(bot))
