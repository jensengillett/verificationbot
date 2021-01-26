import os.path as osp
import random

import discord
from discord.ext import commands
from discord.ext.commands import errors as cmderr

from util.config import BotConfig
# from util.data.guild_data import GuildData  # for reactors

print("Starting...")

current_dir = osp.dirname(__file__)  # grab the current system directory on an os-independent level
data_path = "/app/data"  # folder name

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
	config = BotConfig(config_path)
	config_data = config.data

	bot_data = config_data["bot"]
	bot_token = bot_data["token"]
	bot_key = bot_data["key"]
	used_emails = bot_data["used_emails"]
	# warn_emails = bot_data["warn_emails"]
	# moderator_email = bot_data["moderator_email"]

	# email_data = config_data["email"]
	# sample_username = email_data["sample"]
	# verify_domain = email_data["domain"]
	# email_from = email_data["from"]
	# email_password = email_data["password"]
	# email_subject = email_data["subject"]
	# email_server = email_data["server"]
	# email_port = email_data["port"]

	# discord_data = config_data["discord"]
	# role = discord_data["server_role"]
	# channel_id = discord_data["channel_id"]
	# notify_id = discord_data["notify_id"]
	# admin_id = discord_data["admin_id"]
	# author_name = discord_data["author_name"]

	do_run = config.do_run
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
