import os
from discord.ext import commands

from util.email import is_valid_email


class Background(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		try:
			self.channel_id = os.environ["channel_id"]
		except KeyError as e:
			print(f"Key not loaded!\n\t{e}")

	@commands.Cog.listener("on_message")
	async def on_message(self, message):

		if message.author.bot:
			return

		channel = message.channel
		content = str(message.content).lower()

		if str(channel.id) == str(self.channel_id):
			email_cmd = self.bot.get_command("email")
			cmd_aliases = email_cmd.aliases

			for a in cmd_aliases:
				a = str(a).lower()
				if content.startswith(a):
					content = content.replace(f"{a} ", "", 1)
					break

			if is_valid_email(content):
				ctx = await self.bot.get_context(message)
				return await ctx.invoke(email_cmd, content)


def setup(bot):
	bot.add_cog(Background(bot))
