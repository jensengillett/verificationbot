FROM python:3
WORKDIR /app

# allows better caching of image layers
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

CMD [ "python", "./bot.py" ]
