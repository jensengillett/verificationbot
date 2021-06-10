FROM python:3
WORKDIR /app

RUN pip install discord.py
RUN pip install varint
RUN pip install sqlalchemy

# A bunch of environment variables, will be used in Docker Compose
# bot
ENV token=
ENV key=
ENV used_emails=
ENV warn_emails=
ENV hash_key=
ENV moderator_email=

# email
ENV sample=
ENV domain=
ENV from=
ENV password=
ENV subject=
ENV server=
ENV port=
ENV webmail_link=

# discord
ENV server_role=
ENV channel_id=
ENV notify_id=
ENV admin_id=
ENV author_name=

COPY . /app

CMD [ "python", "./bot.py" ]
