import os.path as osp
import os
import smtplib
import ssl
import random

import discord
from discord.ext import commands
from discord.ext.commands import errors as cmderr

from util.data.guild_data import GuildData  # for reactors

print("Starting...")

current_dir = osp.dirname(__file__)  # grab the current system directory on an os-independent level
data_path = "/data"  # folder name

# The extensions ("cogs") to load
extensions = ["reactor", "utility", "verification"]

# Load new intents system. This is required for the new reactors functionality.
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.reactions = True

# Start the bot functions.
do_run = True

# Start config loading from disk.
try:
	print("Loading config...")

	bot_token = os.environ["token"]
	bot_key = os.environ["key"]
	used_emails = os.environ["used_emails"]
	warn_emails = os.environ["warn_emails"]
	moderator_email = os.environ["moderator_email"]

	sample_username = os.environ["sample"]
	verify_domain = os.environ["domain"]
	email_from = os.environ["from"]
	email_password = os.environ["password"]
	email_subject = os.environ["subject"]
	email_server = os.environ["server"]
	email_port = os.environ["port"]

	role = os.environ["server_role"]
	channel_id = os.environ["channel_id"]
	notify_id = os.environ["notify_id"]
	admin_id = os.environ["admin_id"]
	author_name = os.environ["author_name"]

	channel_id = int(channel_id)
	notify_id = int(notify_id)
	admin_id = int (admin_id)

	do_run = True
except KeyError as e:
	print(f"Config error.\n\tKey Not Loaded: {e}")
	do_run = False

# Seed the random number generator from the bot token.
random.seed(bot_token)

# From the used_emails filename, load the data from the data folder. This can be commented out if not using a data folder.
used_emails = osp.join(current_dir, data_path, used_emails)

# Set up the bot based on the loaded bot prefix and load the intents system.
bot = commands.Bot(command_prefix=bot_key, intents=intents)
# Set's an attr for the bot config path so the verification cog can use it
setattr(bot, "config_path", config_path)

# By default, there's no help command other than vhelp. This is so that it doesn't interfere with other bots using the same prefix.
bot.remove_command('help')


# Update discord presence when everything is successfully loaded.
@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Activity(name="verifications", type=discord.ActivityType.watching))
	print(f'We have logged in as {bot.user}')


# Set up per-message checks.
@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	await bot.process_commands(message)


# Exception handling.
# @bot.event
# async def on_command_error(ctx, exception):
# 	if isinstance(exception, cmderr.PrivateMessageOnly):
# 		await ctx.send("Please DM the bot to use this command!")
# 	elif isinstance(exception, cmderr.NoPrivateMessage):
# 		await ctx.channel.send("This command must be used in a Discord server!")
# 	elif isinstance(exception, cmderr.MissingRole):
# 		await ctx.channel.send("Missing required role to use this command!")
# 	elif isinstance(exception, cmderr.MissingRequiredArgument):
# 		await ctx.channel.send("Missing required arguments!")
# 	else:
# 		print(exception)	


if __name__ == "__main__":

    count = 0
    for extension in extensions:
        try:
            bot.load_extension(f"cogs.{extension}")
            print(f"Cog | Loaded {extension}")
            count += 1
        except Exception as error:
            print(f"{extension} cannot be loaded. \n\t[{error}]")

    print(f"Loaded {count}/{len(extensions)} cogs")

if do_run:
	bot.run(bot_token)
else:
	print("Startup aborted.")
