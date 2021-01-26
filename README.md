# jensengillett/verificationbot
Discord verification bot designed for postsecondary institutions. Fully modular and configurable.

# Background
This project started as a small project for the UVic Engineering and Computer Science Discord server. With a growing server population, we wanted to make an automated system to stop non-UVic students from accessing the remainder of the Discord server. It was with this goal in mind that this bot was initially created.

As the bot has been an effective stopgap for keeping trolls and non-UVic students out of our Discord server, other servers started to take notice. Thanks to the Fall 2020 semester being fully online, many Discord servers popped up, some with thousands of members, and the lack of a verification system has become a concern.

The bot code was therefore rewritten to be fully modularized; every aspect that is necessary to control is located within the *config.toml* file created by the bot.

The main thing to keep in mind is that this bot relies on *email* as the form of verification, and therefore is only realistically applicable to secondary/post-secondary groups who have a mandated and standardized email system.

# Setup
To start, check that you have docker installed. If not, go to https://docs.docker.com/get-docker/ to download docker (and if on Linux or WSL, download docker-compose as well at here: https://docs.docker.com/compose/install/).

Download the docker-compose.yml from above and move it to your folder of choice. Open it with notepad or another text editor and add your bot token, email, etc.

Open a terminal/command prompt and change directory to the folder with the downloaded file and run:
```bash
docker-compose up -d
```
Congratulations! Assuming your variables in the docker-compose file are correct, you should have a running discord bot!

# Commands
Here is a full list of the commands the bot offers:
- vhelp: Displays an information message about how to use the email and verify commands.
- email [email@email.com]: Sends a verification email to a provided email account.
- verify [token]: Uses the token sent to the email account to verify the user.
- prune [x]: (Manage Server only) Prunes the most recent x amount of messages in a channel.
- reactoradd [messageid] [roleid] [emote]: (Manage Server only) Adds a reactor to a message.
- reactordelete [messageid]: (Manage Server only) Removes all reactors from a message.
- reactorget: (Manage Server only) Gets all reactors in the server.
- reactorclearall: (Manage Server only) Removes all reactors in the server.

# Contributors
Notable contributors are listed below:

[aabuelazm](https://github.com/aabuelazm): wrote the Dockerfile for the bot so it can be easily deployed to any Docker-running server as a VM.

[MiningMark48](https://github.com/MiningMark48): wrote the initial draft of the bot code, the *reactor.py* and *util/data/* handlers to work with sqlalchemy, and changed the config system to use TOML.

# License
The code for this repo is licensed under the GPL3. More information can be found in the *LICENSE* file in this repo.

# Notice
This repo is being given very limited support. If Discord's API changes suddenly, do not expect an update for this bot immediately. Major security patches and API changes may result in an update, or may result in support being dropped. If support is dropped indefinitely, this file will be updated to note that the bot is now deprecated.
