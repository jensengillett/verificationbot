# VerificationBot
![License](https://img.shields.io/github/license/jensengillett/verificationbot?color=6cc644&label=License&style=flat-square)
![Repo Stars](https://img.shields.io/github/stars/jensengillett/verificationbot?color=6e5494&label=Stars&logo=github&logoColor=white&style=flat-square)

<!-- Social Shields -->
<!-- [![Twitter](https://img.shields.io/twitter/follow/dakaosjr?color=1da1f2&label=Follow%20@dakaosjr&logo=twitter&logoColor=white&style=flat-square)](https://twitter.com/intent/follow?screen_name=dakaosjr)
[![Twitter](https://img.shields.io/twitter/follow/miningmark48?color=1da1f2&label=Follow%20@miningmark48&logo=twitter&logoColor=white&style=flat-square)](https://twitter.com/intent/follow?screen_name=miningmark48) -->

> A Discord verification bot that is designed for post-secondary institutions. Fully modular and configurable.

- [VerificationBot](#verificationbot)
	- [About](#about)
		- [Background](#background)
		- [How Does it Work?](#how-does-it-work)
- [Setup](#setup)
	- [Docker](#docker)
	- [Python Virtual Environment](#python-virtual-environment)
- [Commands](#commands)
	- [Command Notes](#command-notes)
		- [Email](#email)
- [Contributors](#contributors)
- [Support Development](#support-development)
- [Notice](#notice)
	- [Legal](#legal)
		- [License](#license)
		- [Disclaimer](#disclaimer)

---
## About
### Background
VerificationBot started as a small project for the UVic Engineering and Computer Science Discord server due to a growing server population. We wanted to make an automated system to prevent non-UVic students from accessing the remainder of the Discord server. With this goal in mind, and with the help of [MiningMark48](https://github.com/miningmark48), the initial draft of the bot was created.

Since its initial creation, the bot has been an excellent method for keeping non-UVic students from accessing our Discord server. With our goal accomplished, other servers began to take notice. Thanks to the Fall 2020 semester being fully online due to the pandemic, many more Discord servers were being created, some with thousands of members. With these numerous servers, a lack of a verification system was becoming a concern. 

From this point, the bot was rewritten; going from a single-file bot to a multiple-file, fully modularized machine. What once wasn't possible, the bot was now able to be controlled better than before, thanks to the use of a [config](./docker-compose.yml).

### How Does it Work?
When users join a Discord server, they are given access to limited channels, one of which allows them to send in their university or institutional email with the help of a bot command.

`!email example@example.com`

Once they run the command and if the email is valid (matches the set domain), they will receive an email containing a 4-digit code. The user then takes this code back to the Discord server and runs a command with this code.

`!verify 1234`

If the code is valid, they will be given a role, allowing access to the rest of the server (or however configured).

---

# Setup
## Docker
**Recommended Method**
1. To start, verify Docker is installed. If it is not or you don't know, go [here](https://docs.docker.com/get-docker/) to download Docker. Also, if on Linux or WSL, download the `docker-compose.yml` [here](https://docs.docker.com/compose/install/).

2. Download the `docker-compose.yml` from above and move it to a desired directory. Open it with notepad or your text editor of choice and add your environmental variables (token, key, domain, etc.).

3. A bot token needs to be created to run this bot. You can find the Discord Developers Portal [here](https://discord.com/developers/applications). If you need help making a bot account, [Google](https://letmegooglethat.com/?q=how+to+make+a+discord+bot) is your friend.

	When adding your bot to your server, **make sure the bot has the necessary permissions or things may break!**

	Permissions **required**:
	- Manage Server
	- Manage Roles
	- View Channels
	- Send Messages
	- Manage Messages
	- Read Message History
	- Add Reactions

4. Open a command prompt or terminal, move to the directory containing the  downloaded `docker-compose.yml` file, and run the following command:
	```bash
	docker-compose up -d
	```

5. Congratulations! Assuming your variables in the `docker-compose.yml` file are correct and everything is installed correctly you should have a running Discord bot!

## Python Virtual Environment
1. To start, download this repo. Also, ensure you have Python 3.7+ installed.

2. Create a virtual environment with the following command:
	```bash
	python -m venv venv
	```

3. Activate the virtual environment with one of the following commands:
	```bash
	.\venv\Scripts\activate
	```
	or
	```bash
	activate venv
	```

4. Install dependencies found in `requirements.txt`:
	```bash
	pip install -r requirements.txt
	```

5. Create a `.env` file in the same directory as the downloaded repo. In this file, set your environmental variables as specified in `docker-compose.yml`.

6. Finally, run `bot.py`:
   ```bash
   python boy.py
   ```

7. Congratulations! Assuming all went well and everything is installed correctly you should have a running Discord bot!

---

# Commands
Here is a full list of the commands the bot offers:

| Command | Description | Permissions Required | Usage* |
|---------|-------------|----------------------|-------|
| vhelp | Displays an informative message about how to use the email and verify commands. | None | vhelp |
| email | Sends a verification email to a provided email account. | None | email <email: str> |
| verify | Uses the token sent to the email account to verify the user. | None | verify <token: int> |
| support | Replies with links to financially and socially support the authors and contributors of this bot | None | support |
| prune | Prunes the most recent *n* amount of messages in a channel. | Manage Server | prune <amount: int> |
| reactoradd | Adds a reactor to a message | Manage Server | reactoradd <message_id: str> <role_id: str> <emote: emote> |
| reactordelete | Removes all reactors from a message. | Manage Server | reactordelete <message_id: str> |
| reactorget | Get all reactors in the server | Manage Server | reactorget |
|reactorclearall | Removes all reactors in the server. | Manage Server | reactorclearall |

\* `<>` = required, `[]` = optional

## Command Notes
### Email
There are a variety of extra handlers to help aid people that can't quite follow the instructions properly. The email command will accept the following variations:
- (!) email [email@email.com]  - extra space before 'email'
- (!)[email@email.com]  - no 'email'
- (!)email[email@email.com]  - missing space between 'email' and their email
- [email@email.com]  - missing alias and 'email'
- email [email@email.com]  - missing alias

These are primarily there to assist people new to Discord or who can't follow instructions. The *vhelp* command encourages use of the proper form, \<alias>email [email@email.com].

---

# Contributors
Notable contributors are listed below:

| Contributor | Contribution |
|-------------|--------------|
| [MiningMark48](https://github.com/MiningMark48) | Wrote the initial draft of the bot, reactor module, and data handlers to integrate to [sqlalchemy](https://pypi.org/project/SQLAlchemy/), rewrote the bot to use [Discord.py *Cogs*](https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html), and implemented miscellaneous commands and features. |
| [aabuelazm](https://github.com/aabuelazm) | Wrote the [Dockerfile](/Dockerfile) and implemented environmental variables to `bot.py` for easy Docker container deployment. |
| [MNThomson](https://github.com/MNThomson) | Fixed vulnerabilities |

---

# Support Development
If you use this bot on your server, feel free to credit me by linking to this repository. 

If you want to support me financially, [buy me a cup of coffee](https://ko-fi.com/jensengillett)! 

You can also support me through [PayPal](https://paypal.me/jensengillett) directly.

# Notice
## Legal
### License
The code for this repo is licensed under the GPL3. More information can be found in the [LICENSE file](/LICENSE) in this repo.

### Disclaimer
This project is not affiliated with [Discord](https://discord.com/) or [discord.py](https://github.com/Rapptz/discord.py).

**Future Updates**

Although this repo is being given support and updates, it is limited. If [Discord](https://discord.com/) or [discord.py](https://github.com/Rapptz/discord.py) make any sudden changes to their API, do not expect an immediate update. 

Major security patches and API changes may result in an update, or may result in support being dropped. If support is dropped indefinitely, this file will be updated to note that the bot is now deprecated and the repo will be archived and set to read-only. At the moment, this is unlikely and not in the forseeable future.

---
