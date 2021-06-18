from os import name
import discord
from discord.ext import commands


class Misc(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		self.github_link = "https://github.com/jensengillett/verificationbot"

	@commands.command(aliases=["coffee", "buymeacoffee", "paypal", "pp", "cashapp", "source"])
	async def support(self, ctx):
		"""Support development!"""

		embed = discord.Embed(title="Support", color=0x00ff00)
		embed.description = f"[Repository]({self.github_link})"
		embed.timestamp = ctx.message.created_at

		disc_jensen = """
		Project Owner, Contributor, Maintainer
		[Ko-fi](https://ko-fi.com/jensengillett)
		[PayPal](https://paypal.me/jensengillett)
		"""
		embed.add_field(name="Jensen", value=disc_jensen, inline=False)

		desc_mark = """
		Contributor, Maintainer, Initial Author
		[Ko-fi](https://ko-fi.com/miningmark48)
		[CashApp](https://cash.app/$MiningMark48)
		"""
		embed.add_field(name="Mark", value=desc_mark, inline=False)

		# desc_aabuelazm = """
		# Contributor, Maintainer
		# LINKS TBD
		# """
		# embed.add_field(name="aabuelazm", value=desc_aabuelazm, inline=False)

		await ctx.reply(embed=embed)


def setup(bot):
	bot.add_cog(Misc(bot))
