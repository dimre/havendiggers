# Twitter Telegram Chatbot

## Starting in local 💻

### System requirements
- [Python 3](https://www.python.org/downloads/)

### Install with *pip3*
```bash
pip3 install -r requirements.txt
```

### Steps
```bash
py main.py # windows
python3 main.py # linux
```

## Starting with docker 🐳

#### System requirements
- [Docker](https://www.docker.com/get-started)

### Steps
```bash
docker build --tag botimage .
docker run -d --name botcontainer botimage
```
To stop/remove the container:
```bash
docker stop botcontainer # stop the container
docker rm -f botcontainer # remove the container
```

## Starting on Heroku 🌐
Create an heroku app and load the application. This can be done in many ways.  
One easy way to do it is to use the github action provided in _.github/workflows/python-app.yml_  
Make sure you have an heroku account and a Github account.  
Create an heroku app, and start creating following enviroment variables: "TELEGRAM_TOKEN", "TWITTER_API_KEY", "TWITTER_API_KEY_SECRET", "TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_TOKEN_SECRET".  
Create the github repository and push the whole repository. Add the following secrets to the github repository: "HEROKU_API_KEY", "APP_NAME", "EMAIL".
Make sure to remove any of the sensitive data listed above by the _config/settings.yaml_ file and push the repository.
Add the following enviroment variable on the heroku app:
```bash
WEBHOOK_URL=https://<app-name>.herokuapp.com/ # insert the name you give to the app
```
Since heroky apps are ephemeral, you will also need to create a database to store the data. You can use the integrated Heroku Postgres add-on.

## Settings 🔧
To alter the bot's settings, you need to edit the _config/settings.yaml_ file.  
Whenever this settings change, the bot **must** be rebooted for the changes to be effective.  
Comments must be removed.
```yaml
twitter_user_list: # list of twitter users the bot will check for (without @)
  - "name1"
  - "name2"
telegram_user_list: # list of telegram ids of users allowed to use the bot and that the bot will notify
  - 1111111111 # positive number for a user
  - -44444444 # negative number for a group
twitter_api_key: "XXXXXXXXX" # twitter consumer Key
twitter_api_key_secret: "XXXXXXXXXXXXXXXXXXXXXX" # twitter consumer key secret
twitter_access_token: "XXXXXXXXXXXXXXXXXXXXXXXXXXX" # twitter api access token
twitter_access_token_secret: "XXXXXXXXXXXXXXXXXXXXXXX" # twitter api access token secret
telegram_token: "XXXXXXXXXXXXXXXXXXXXXXX" # token of the telegram bot
loop_time: 900 # number of seconds between each check. If the previous one hasn't finished yet, the current check will be skipped
```

By default, the bot will use a local database.  
If an enviromend variable named **"DATABASE_URL"** is present, its value is used to connet to a postgres database.