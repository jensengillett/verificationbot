from discord.ext import commands
import time
import datetime


class Utility(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# noinspection PyGlobalUndefined
	@commands.Cog.listener()
	async def on_ready(self):
		global start_time  # global variable for uptime
		start_time = time.time()  # store current time

	@commands.command(name="prune", aliases=["purge", "nuke", "Prune", "Purge", "Nuke"])
	@commands.has_permissions(manage_messages=True)
	@commands.guild_only()
	async def prune(self, ctx, amt: int):
		"""Bulk delete messages (up to 100)"""

		amt = max(min(amt, 100), 0)  # Clamp between 0 and 100
		await ctx.message.delete()
		await ctx.channel.purge(limit=amt)
		msg = await ctx.send(f'Pruned `{amt}` messages.')
		await msg.delete(delay=3)

	@commands.command(name="uptime", aliases=["Uptime", "up-time", "Up-time", "up", "time", "Up", "Time"])
	async def uptime(self, ctx):
		"""Check how long the bot script has been running for.
		Thanks to https://stackoverflow.com/questions/62483161/discord-py-uptime"""

		uptime = str(datetime.timedelta(seconds=int(round(time.time()-start_time))))
		await ctx.send(f"This bot has been running for {uptime}.")


def setup(bot):
	bot.add_cog(Utility(bot))
