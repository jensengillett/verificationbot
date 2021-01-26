import discord
from discord.ext import commands


class Errors(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# Exception handling.
	@commands.Cog.listener("on_command_error")
	async def on_command_error(ctx, exception):
		if isinstance(exception, cmderr.PrivateMessageOnly):
			await ctx.send("Please DM the bot to use this command!")
		elif isinstance(exception, cmderr.NoPrivateMessage):
			await ctx.channel.send("This command must be used in a Discord server!")
		elif isinstance(exception, cmderr.MissingRole):
			await ctx.channel.send("Missing required role to use this command!")
		elif isinstance(exception, cmderr.MissingRequiredArgument):
			await ctx.channel.send("Missing required arguments!")
		else:
			print(exception)


def setup(bot):
    bot.add_cog(Errors(bot))