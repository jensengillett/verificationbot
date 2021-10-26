import os
from discord.ext import commands

from util.email import is_valid_email


# This handler handles some edge cases where people are being very stupid.
# Namely, for emails it handles if someone misses the command key. (If they use the command key properly but screw up elsewhere, the handler is in errors.py.)
# For any message that is not a recognizable email or mangled command, it simply prints vhelp instead.
# The fact that this has to exist is very sad.
class Background(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		try:
			self.channel_id = os.environ["channel_id"]  # grab verification channel ID so we know which channel to watch
		except KeyError as e:
			print(f"Key not loaded!\n\t{e}")  # bad user

	# This triggers on every message across the whole server. This isn't normally a performance problem in the intended use case (a single university server) but may have scalability issues.
	# Note that this doesn't happen on valid commands, which *is a side effect* due to the way discord.py functions. If the way commands are handled changes, this code will likely break!
	@commands.Cog.listener("on_message")
	async def on_message(self, message):

		if message.author.bot:  # ignore bots
			return

		channel = message.channel
		content = str(message.content).lower()  # ignore case sensitivity, it doesn't matter for emails anyway

		if str(channel.id) == str(self.channel_id):  # check if we're in the right channel
			# grab the email command so we can check the aliases list
			email_cmd = self.bot.get_command("email")
			cmd_aliases = email_cmd.aliases

			# if any of the email command aliases is present, then we fix up the command and send it off to is_valid_email
			for a in cmd_aliases:
				a = str(a).lower()
				if content.startswith(a):
					content = content.replace(f"{a} ", "", 1)
					break

			# get the message context to pass on
			ctx = await self.bot.get_context(message)

			if is_valid_email(content):  # check if we're dealing with an email
				return await ctx.invoke(email_cmd, content)  # invoke the email command with the fixed arguments
			else:  # not an email
				vhelp_cmd = self.bot.get_command("vhelp")  # grab the vhelp command
				return await ctx.invoke(vhelp_cmd, content)  # invoke the vhelp command for our poor users


def setup(bot):
	bot.add_cog(Background(bot))
