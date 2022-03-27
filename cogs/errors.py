import copy
# from re import VERBOSE

# import discord
# from discord.errors import InvalidArgument
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
		elif isinstance(exception, cmderr.UserInputError):
			await ctx.channel.send("Missing or invalid argument!")
		elif isinstance(exception, cmderr.CommandNotFound):

			message_content = ctx.message.content.replace(ctx.prefix, "")

			def clean_aliases(message_content: str, aliases: list):
				for a in aliases:
					a = str(a).lower()
					if message_content.startswith(a):
						message_content = message_content.replace(f"{a} ", "", 1)
						message_content = message_content.replace(a, "", 1)
						break
				return message_content

			async def invoke_cmd(ctx, cmd, message_content):
				msg = copy.copy(ctx.message)
				msg.content = message_content
				ctx = await self.bot.get_context(msg)
				await ctx.invoke(cmd, message_content)

			# If the attempted command is a valid email, run the email command
			email_cmd = self.bot.get_command("email")
			message_content = clean_aliases(message_content, email_cmd.aliases)

			if is_valid_email(message_content):
				return await invoke_cmd(ctx, email_cmd, message_content)

			verify_cmd = self.bot.get_command("verify")
			message_content = clean_aliases(message_content, verify_cmd.aliases)

			if len(message_content) == 4 and message_content.isnumeric():
				return await invoke_cmd(ctx, verify_cmd, message_content)

		else:
			print(exception)


def setup(bot):
	bot.add_cog(Errors(bot))
