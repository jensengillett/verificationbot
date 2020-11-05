FROM python:3

RUN pip install discord.py
RUN pip install varint
RUN pip install sqlalchemy

WORKDIR /app

COPY . /app

CMD [ "python", "./bot.py" ]
