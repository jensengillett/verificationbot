# jensengillett/verificationbot
Discord verification bot. Fully modular and configurable.

# Background
This project started as a small project for the UVic Engineering and Computer Science discord. With a growing server population, we wanted to make an automated system to stop non-UVic students from accessing the remainder of the Discord server. It was with this goal in mind that this bot was initially created.

As the bot has been an effective stopgap for keeping trolls and non-UVic students out of the discord servers, other servers started to take notice. Thanks to the Fall 2020 semester being fully online, many discord servers popped up, some with thousands of members, and the lack of a verification system has become a concern.

The bot code was therefore rewritten to be fully modularized; every aspect that is necessary to control is located within the *config.json* file created by the bot.

The main thing to keep in mind is that this bot relies on *email* as the form of verification, and therefore is only realistically applicable to secondary/post-secondary groups who have a mandated and standardized email system.

# Setup
To start, clone this repo. Everything you need is included.

Deploy the bot to whichever server you plan to use; if that's a Docker server, the Dockerfile will automatically configure the container for you. PLEASE NOTE: If you're doing this, make sure that the */data/* folder created by the bot is persistent! Otherwise if you redeploy later everything (ie the email list and reactors) will be lost!

Upon first run of *bot.py*, the bot will notice the missing config.json file and create one for you. This file is the only file that needs to be edited for operation. Descriptions of each setting are availible at the top of the *bot.py* script.

A bot token needs to be created to run this bot. The Discord Developers Portal is linked here: https://discord.com/developers/applications. Google is your friend. The permissions required for this bot are *Manage Server*, *Manage Roles*, *View Channels*, *Send Messages*, *Manage Messages*, *Read Message History*, and *Add Reactions*. 

# License
The code for this repo is licensed under the GPL3. More information can be found in the *LICENSE* file in this repo.

# Contributors
Notable contributors are listed below:
aabuelazm: wrote the Dockerfile for the bot so it can be easily deployed to any Docker-running server as a VM.
MiningMark48: wrote the initial draft of the bot code and the *reactor.py* and *util/data/* handlers to work with sqlalchemy.
