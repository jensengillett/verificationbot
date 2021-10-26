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

			# If the attempted command is a valid email, run the email command
			email_cmd = self.bot.get_command("email")
			content = clean_aliases(content, email_cmd.aliases)

			if is_valid_email(content):
				return await invoke_cmd(email_cmd, content)

			verify_cmd = self.bot.get_command("verify")
			content = clean_aliases(content, verify_cmd.aliases)

			if len(content) == 4 and content.isnumeric():
				return await invoke_cmd(verify_cmd, content)


def setup(bot):
	bot.add_cog(Background(bot))
