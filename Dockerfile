FROM python:3
WORKDIR /app

RUN pip install discord.py
RUN pip install varint
RUN pip install sqlalchemy
RUN pip install toml

COPY . /app

CMD [ "python", "./bot.py" ]
