import os
import asyncio

import discord
from discord.ext import commands
from discord.ext.commands.converter import clean_content

from util.email import is_valid_email


class VerifyWizard(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		self.timeout = 10
		self.in_convo = list()

		try:
			self.channel_id = os.environ["channel_id"]
		except KeyError as e:
			print(f"Key not loaded!\n\t{e}")

	@commands.Cog.listener("on_message")
	async def on_message(self, message):

		channel = message.channel
		author = message.author
		prune_messages = list()

		def check(m):
			return m.author == author and m.channel == channel

		async def abort():
			self.in_convo.remove(author.id)
			await self.prune(prune_messages)
			return await message.reply("It's ok! I'm here if you need me!", delete_after=10)

		def is_yes(answer: str):
			return answer.lower() in ["yes", "y"]

		if message.author.bot:
			return

		if str(channel.id) != str(self.channel_id):
			return

		if author.id in self.in_convo:
			return

		self.in_convo.append(author.id)
		wizard_msg = await message.reply("Hello! Are you trying to verify your account? [Yes (Y) / No (N)]")
		prune_messages.append(wizard_msg)
		prune_messages.append(message)

		try:
			response = await self.bot.wait_for('message', check=check, timeout=self.timeout)
		except asyncio.TimeoutError:
			return await abort()

		cleaned_response = response.clean_content.lower()
		prune_messages.append(response)

		if is_yes(cleaned_response):  	# Response == Yes
			wizard_msg = await response.reply("Have you received a verification email yet? [Yes (Y) / No (N)]")
			prune_messages.append(wizard_msg)

			try:
				response = await self.bot.wait_for('message', check=check, timeout=self.timeout)
			except asyncio.TimeoutError:
				return await abort()

			cleaned_response = response.clean_content.lower()
			prune_messages.append(response)

			if is_yes(cleaned_response):
				wizard_msg = await response.reply("Awesome! What is your verification token? This can be found in the email.")
				prune_messages.append(wizard_msg)

				try:
					response = await self.bot.wait_for('message', check=check, timeout=self.timeout)
				except asyncio.TimeoutError:
					return await abort()

				cleaned_response = response.clean_content.lower()
				prune_messages.append(response)

				if len(cleaned_response) != 4 or not cleaned_response.isnumeric():
					self.in_convo.remove(author.id)
					return await response.reply("That's not a valid token!", delete_after=10)

				email_cmd = self.bot.get_command("verify")
				ctx = await self.bot.get_context(message)
				await ctx.invoke(email_cmd, cleaned_response)

				self.in_convo.remove(author.id)

			else:
				wizard_msg = await response.reply("That's ok! What is your email?")
				prune_messages.append(wizard_msg)

				try:
					response = await self.bot.wait_for('message', check=check, timeout=self.timeout)
				except asyncio.TimeoutError:
					return await abort()

				cleaned_response = response.clean_content.lower()
				prune_messages.append(response)

				if not is_valid_email(cleaned_response):
					self.in_convo.remove(author.id)
					return await response.reply("That's not a valid email!", delete_after=10)

				email_cmd = self.bot.get_command("email")
				ctx = await self.bot.get_context(message)
				await ctx.invoke(email_cmd, cleaned_response, True)

				wizard_msg = await response.reply("The email has been sent! Come back to me once you have received it!")
				prune_messages.append(wizard_msg)
				self.in_convo.remove(author.id)

			await self.prune(prune_messages)

		else:
			return await abort()

		await self.prune(prune_messages)

	async def prune(self, prune_messages: list):
		for msg in prune_messages:
			try:
				await msg.delete()
			except discord.errors.NotFound:
				pass
			await asyncio.sleep(0.5)


def setup(bot):
	bot.add_cog(VerifyWizard(bot))
