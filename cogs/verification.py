import os
import smtplib
import ssl
import random

import discord
from discord.ext import commands


class Verification(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		try:
			# bot_token = os.environ["token"]
			self.bot_key = os.environ["key"]
			self.used_emails = os.environ["used_emails"]
			self.warn_emails = os.environ["warn_emails"]
			self.moderator_email = os.environ["moderator_email"]

			self.sample_username = os.environ["sample"]
			self.verify_domain = os.environ["domain"]
			self.email_from = os.environ["from"]
			self.email_password = os.environ["password"]
			self.email_subject = os.environ["subject"]
			self.email_server = os.environ["server"]
			self.email_port = os.environ["port"]

			self.role = os.environ["server_role"]
			self.channel_id = os.environ["channel_id"]
			self.notify_id = os.environ["notify_id"]
			self.admin_id = os.environ["admin_id"]
			self.author_name = os.environ["author_name"]

			self.channel_id = int(self.channel_id)
			self.notify_id = int(self.notify_id)
			self.admin_id = int(self.admin_id)

		except KeyError as e:
			print(f"Config error.\n\tKey Not Loaded: {e}")

		# Create empty lists for currently active tokens, emails, and attempt rejection.
		self.token_list = {}
		self.email_list = {}
		self.email_attempts = {}
		self.verify_attempts = {}

	# Instructions on how to verify.
	@commands.command(name="vhelp", aliases=["helpme", "help_me", "verify_help", "Vhelp", "Helpme", "Help_me", "Verify_help"])
	async def verify_help(self, ctx):
		"""
		Help on how to verify.
		"""
		verify_email = ctx.guild.get_channel(self.channel_id)
		# The line below contains the verify_help command text output.
		await ctx.send(
			f"To use this bot, please use `{self.bot_key}email {self.sample_username}@{self.verify_domain}` in {verify_email.mention} "
			f"to receive an email with a **4 digit verification token.** Replace `{self.sample_username}@{self.verify_domain}` with "
			f"your own email, keeping in mind that the bot only accepts email addresses with `@{self.verify_domain}` at the end. "
			f"**Wait for an email to be received**. If you don't receive an email after 5 minutes, try using the email "
			f"command again. **Send the command provided in the email** as a message in the {verify_email.mention} channel "
			f"to gain access to the rest of the server.\n\n**Send messages in the {verify_email.mention} channel to use this "
			f"bot's commands, not in a DM.**")

	# The email command handles all the checks done before an email is sent out alongside the actual email sending.
	# It's very complicated.
	@commands.command(name="email", aliases=["mail", "send", "Email", "Mail", "Send"])
	async def _email(self, ctx, arg):
		if ctx.channel.id == self.channel_id:
			"""
			Sends an email containing a token to verify the user
			Parameters
			------------
			email: str [Required]
				The email that the token will be send to.
			"""
			print(f'Emailing user {ctx.author.name}, email {arg}')  # This gets sent to the console only.
			await ctx.message.delete()  # delete their email from the channel, to prevent it leaking.

			dm = "teststring"  # just in case, though this should never actually get used.

			try:
				dm = arg.split('@')[1]  # split the string based on the @ symbol
			except:
				await ctx.send("Error! That is not a valid email!")  # no @ symbol = no email

			if set('+').intersection(arg):  # to prevent people from making extra email addresses
				dm = "nou"
				await ctx.send("Error! Please do not use the + character in your email address!")

			blacklist_names = [self.sample_username]  # If any email begins with one of these, it's invalid

			if any(arg.lower().startswith(name.lower()) for name in blacklist_names):
				await ctx.send(
					f"{ctx.author.mention} Use your own email, not the sample one. Please try again with your own email.")
				return

			try:
				with open(self.used_emails, 'r') as file:  # Checks the used emails file to see if the email has been used.
					if any(str(arg.lower()) == str(line).strip('\n').lower() for line in file):
						admin = await self.bot.fetch_user(self.admin_id)
						await ctx.send(
							f"Error! That email has already been used! If you believe this is an error or are trying to "
							f"re-verify, please contact {admin.mention} in this channel or through direct message. Thanks!")
						return
			except FileNotFoundError:
				print("Used emails file hasn't been created yet, continuing...")

			try:
				with open(self.warn_emails, 'r') as file:  # Checks the warning email file to notify moderators if an email on the list is used. For example, a list of professor emails could be loaded.
					if any(str(arg.lower()) == str(line).strip('\n').lower() for line in file):
						sendIn = ctx.guild.get_channel(self.notify_id)
						await sendIn.send(
							f"Alert! Email on warning list used. Discord ID: {ctx.author.mention}, email `{arg}`.")
			except FileNotFoundError:
				print("Warning list file not found, ignoring rest.")

			# This is a bit of a hacky way to do an email attempt checking system. If someone tries to repeatedly use the email command, they will be blacklisted from further attempts.
			maxedOut = False
			try:
				if self.email_attempts[ctx.author.id] >= 5:
					maxedOut = True
					await ctx.send(
						f"{ctx.author.mention}, you have exceeded the maximum number of command uses. Please contact a "
						f"moderator for assistance with verifying if this is in error. Thanks!")
					sendIn = ctx.guild.get_channel(self.notify_id)
					await sendIn.send(f"Alert! User {ctx.author.mention} has exceeded the amount of `!email` command uses.")
					return
			except:
				print("")

			if dm == self.verify_domain and not maxedOut:  # Send the actual email.
				await ctx.send("Sending verification email...")
				with smtplib.SMTP_SSL(self.email_server, self.email_port, context=ssl.create_default_context()) as server:
					server.login(self.email_from, self.email_password)
					token = random.randint(1000, 9999)
					self.token_list[ctx.author.id] = str(token)
					self.email_list[ctx.author.id] = arg
					verify_email = ctx.guild.get_channel(self.channel_id)

					message_text = f"Hello {self.author_name},\n\nThe command to use in {verify_email.name} is: " \
						f"\n\n{self.bot_key}verify {token}\n\nMake sure you paste that entire line into the chat, and press enter to " \
						f"send the message. \n\nThank you for joining our Discord server! \n\nThis message was sent automatically " \
						f"by a bot. If you did not request this message, please contact {self.moderator_email} to report this incident."
					message = f"Subject: {self.email_subject}\n\n{message_text}"
					server.sendmail(self.email_from, arg, message)
					server.quit()

				await ctx.send(f"Verification email sent, do `{self.bot_key}verify ####`, where `####` is the token, to verify.")

				if self.email_attempts:
					if ctx.author.id in self.email_attempts:
						self.email_attempts[ctx.author.id] += 1
					else:
						self.email_attempts[ctx.author.id] = 1
				else:
					self.email_attempts[ctx.author.id] = 1

			else:
				await ctx.send(f"Invalid email {ctx.author.mention}!")

	@commands.command(name="verify", aliases=["token", "Verify", "Token"])
	@commands.guild_only()
	async def _verify(self, ctx, arg):
		"""
		Verifies a user with a token that was previously email.
		For use after the 'email' command.
		Parameters
		------------
		token: int [Required]
			The token that was sent to the user via email.
		"""
		if ctx.channel.id == self.channel_id:
			print(f'Verifying user {ctx.author.name}, token {arg}')
			await ctx.message.delete()

			# this is copied from above to avoid an issue where two people could use the same email before it was verified.
			try:
				with open(self.used_emails, 'r') as file:  # Checks the used emails file to see if the email has been used.
					if any(str(self.email_list[ctx.author.id]) == str(line).strip('\n').lower() for line in file):
						await ctx.send(
							"Error! That email has already been used! If you believe this is an error or are trying to "
							"re-verify, please contact a moderator in this channel or through direct message. Thanks!")
						return
			except FileNotFoundError:
				print("Used emails file hasn't been created yet, continuing...")

			try:
				if self.verify_attempts[ctx.author.id] >= 5:
					await ctx.send(
						f"{ctx.author.mention}, you have exceeded the maximum number of command uses. Please contact a "
						f"moderator for assistance with verifying if this is in error. Thanks!")
					sendIn = ctx.guild.get_channel(self.notify_id)
					await sendIn.send(
						f"Alert! User {ctx.author.mention} has exceeded the amount of `!verify` command uses.")
					return
			except:
				print("")

			if self.token_list:
				if self.token_list[ctx.author.id] == arg:
					await ctx.send(f"{ctx.author.mention}, you've been verified!")
					await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name=self.role))
					with open(self.used_emails, 'a') as file:  # Writes used emails to file for verification
						file.write(f"{self.email_list[ctx.author.id]}\n")
				else:
					await ctx.send(f"Invalid token {ctx.author.mention}!")
					if self.verify_attempts:
						if ctx.author.id in self.verify_attempts:
							self.verify_attempts[ctx.author.id] += 1
						else:
							self.verify_attempts[ctx.author.id] = 1
					else:
						self.verify_attempts[ctx.author.id] = 1

			else:
				print("Array does not exist yet! Verify will return nothing!")


def setup(bot):
	bot.add_cog(Verification(bot))
