FROM python:3
WORKDIR /app

RUN pip install discord.py
RUN pip install varint
RUN pip install sqlalchemy
RUN pip install toml

# A bunch of environment variables, will be used in Docker Compose
# bot
ENV token
ENV key
ENV used_emails
ENV warn_emails
ENV moderator_email

#email
ENV sample
ENV domain
ENV from
ENV password
ENV subject
ENV server
ENV port

#discord
ENV server_role
ENV channel_id
ENV notify_id
ENV admin_id
ENV author_name

RUN echo -e "[bot]\n\
token = \"$token\"\n\
key = \"$key\"\n\
used_emails = \"$used_emails\"\n\
warn_emails = \"$exchange_emails\"\n\
moderator_email = \"$moderator_email\"\n\
\n\
[email]\n\
sample = \"$sample\"\n\
domain = \"$domain\"\n\
from = \"$from\"\n\
password = \"$password\"\n\
subject = \"$subject\"\n\
server = \"$server\"\n\
port = \"$port\"\n\
\n\
[discord]\n\
server_role = \"$server_role\"\n\
channel_id = $channel_id\n\
notify_id = $notify_id\n\
admin_id = $admin_id\n\
author_name = \"$author_name\"" >config.toml

COPY . /app

CMD [ "python", "./bot.py" ]
