from discord.ext import commands


class Misc(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		self.kofi_link = "https://ko-fi.com/jensengillett"
		self.paypal_link = "https://paypal.me/jensengillett"

	@commands.command(aliases=["coffee", "buymeacoffee"])
	async def kofi(self, ctx):
		"""Support development on Ko-Fi!"""

		await ctx.reply(self.kofi_link)

	@commands.command(aliases=["pp"])
	async def paypal(self, ctx):
		"""Support development on PayPal!"""

		await ctx.reply(self.paypal_link)


def setup(bot):
	bot.add_cog(Misc(bot))
