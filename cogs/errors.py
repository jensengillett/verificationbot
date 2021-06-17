import copy

import discord
from discord.ext import commands
from discord.ext.commands import errors as cmderr

from util.email import is_valid_email


class Errors(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# Exception handling.
	@commands.Cog.listener("on_command_error")
	async def on_command_error(self, ctx, exception):
		if isinstance(exception, cmderr.PrivateMessageOnly):
			await ctx.send("Please DM the bot to use this command!")
		elif isinstance(exception, cmderr.NoPrivateMessage):
			await ctx.channel.send("This command must be used in a Discord server!")
		elif isinstance(exception, cmderr.MissingRole):
			await ctx.channel.send("Missing required role to use this command!")
		elif isinstance(exception, cmderr.MissingRequiredArgument):
			await ctx.channel.send("Missing required arguments!")
		elif isinstance(exception, cmderr.CommandNotFound):

			# If the attempted command is a valid email, run the email command
			email = ctx.message.content.replace(ctx.prefix, "")
			if is_valid_email(email):
				ctx = await self.bot.get_context(email)
				cmd = self.bot.get_command("email")
				await ctx.invoke(cmd, email)

		else:
			print(exception)


def setup(bot):
	bot.add_cog(Errors(bot))
