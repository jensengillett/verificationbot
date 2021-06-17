import copy

import discord
from discord.ext import commands
from discord.ext.commands import errors as cmderr


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
				msg = copy.copy(ctx.message)
				channel = ctx.channel
				msg.channel = channel
				msg.author = ctx.author
				msg.content = f"{ctx.prefix}email {email}"
				new_ctx = await self.bot.get_context(msg, cls=type(ctx))
				await self.bot.invoke(new_ctx)
		else:
			print(exception)


def is_valid_email(email: str):
	print("Email ", email)

	try:
		dm = email.split('@')[1]  # split the string based on the @ symbol
	except AttributeError as e:
		print("DM EX\n", e)
		return False

	if not dm:
		print("NOT DM")
		return False

	if len(email.split('@')[0]) > 64 or len(email.split('@')[1]) > 255:  # valid emails have 64char max before @, 255 max after
		print("LEN")
		return False

	if set('+').intersection(email):  # to prevent people from making extra email addresses
		print("+")
		return False

	return True


def setup(bot):
	bot.add_cog(Errors(bot))
