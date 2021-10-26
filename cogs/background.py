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
      
      def clean_aliases(message_content: str, aliases: list):
				for a in aliases:
					a = str(a).lower()
					if message_content.startswith(a):
						message_content = message_content.replace(f"{a} ", "", 1)
						message_content = message_content.replace(a, "", 1)
						break
				return message_content
      
      async def invoke_cmd(cmd, message_content):
				ctx = await self.bot.get_context(message)
				await ctx.invoke(cmd, message_content)
      
			# grab the email command so we can check the aliases list
			email_cmd = self.bot.get_command("email")
      vhelp_cmd = self.bot.get_command("vhelp")  # grab the vhelp command
			content = clean_aliases(content, email_cmd.aliases)

			# get the message context to pass on
			ctx = await self.bot.get_context(message)

			if is_valid_email(content):  # check if we're dealing with an email
				return await invoke_cmd(email_cmd, content)
      
      verify_cmd = self.bot.get_command("verify")
			content = clean_aliases(content, verify_cmd.aliases)

			if len(content) == 4 and content.isnumeric():
				return await invoke_cmd(verify_cmd, content)
			else:  # not an email
				return await invoke_cmd(vhelp_cmd, content)  # invoke the vhelp command for our poor users


def setup(bot):
	bot.add_cog(Background(bot))
