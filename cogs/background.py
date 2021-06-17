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
		channel = message.channel
		content = message.content
		if str(channel.id) == str(self.channel_id):
			if is_valid_email(content):
				ctx = await self.bot.get_context(message)
				cmd = self.bot.get_command("email")
				await ctx.invoke(cmd, content)


def setup(bot):
	bot.add_cog(Background(bot))
