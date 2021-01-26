import discord
from discord.ext import commands


class Utility(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="prune", aliases=["purge", "nuke", "Prune", "Purge", "Nuke"])
	@commands.has_permissions(manage_messages=True)
	@commands.guild_only()
	async def prune(self, ctx, amt: int):
		"""Bulk delete messages (up to 100)"""
		if not amt > 0 and amt <= 100:  # TODO: Clamp this value
			await ctx.send(f'Amount must be between **0** and **100**, you entered `{amt}`')
			return
		await ctx.message.delete()
		await ctx.channel.purge(limit=amt)
		msg = await ctx.send(f'Pruned `{amt}` messages.')
		await msg.delete(delay=3)


def setup(bot):
	bot.add_cog(Utility(bot))
