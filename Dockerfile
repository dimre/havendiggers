FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
#Install requirements
RUN python -m pip install --upgrade pip &&\
  pip3 install -r requirements.txt

COPY . .

#Start the bot
CMD [ "python3", "main.py" ]
