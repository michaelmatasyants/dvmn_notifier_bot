# Notification bot in Telegram

The project allows receiving messages from telegram bot about code review on lessons [dvmn.org](https://dvmn.org/).<br>
The [dvmn API ](https://dvmn.org/api/docs/) is used to get information about the status of lessons.
Also you need to create a telegram bot


## How to install

1. To run the project you should already have Python 3 and pip (package-management system) installed.

2. Download the code (use git clone).
   ```
   git clone git@github.com:michaelmatasyants/dvmn_notifier_bot.git
   ```

3. Create a virtual environment with its own independent set of packages using [virtualenv/venv](https://docs.python.org/3/library/venv.html).
   It'll help you to isolate the project from the packages located in the base environment.

4. Install all the packages used in this project, in your virtual environment which you've created on the step 3. Use the `requirements.txt` file to install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. To use this script, you also need a dvmn API key. To get the API key, go to [API link](https://dvmn.org/api/docs/) from your account.<br>
   Save the bot token in `.env` file like it's done in `.env.example`.

6. Also, to receive messages from the bot, you must first create it.<br>
   In order to do this, find `@BotFather` in `Telegram` and start a new conversation with it. Then send him `/newbot` to create a new Telegram bot and follow the instructions. In the last step, a bot access token will be issued, which you need to save in `.env` file like it's done in `.env.example`.

7. Delete useless file `.env.example`.

8. Find out your chat_id in Telegram, we will need it later. To do this, send a message to the bot `@userinfobot` or press `start` in chat with the bot, and you will get your `chat_id`.

9. Remember to add `.env` to your `.gitignore` if you are going to put the project on GIT.


## Examples of running scripts




Let's take a look at what this script can do first.<br>
Run:
```
python3 main.py -h
```

Output:
```
usage: main.py [-h] chat_id

This script helps to track and check for passed code reviews on dvmn.org. If there are any, the telegram bot sends a message about available code reviews for a particular lesson. To use this script you
only need to specify your chat_id for the telegram where you want to get messages. To get your chat_id, send a message to @userinfobot in telegram.

positional arguments:
  chat_id     Enter, your chat_id

options:
  -h, --help  show this help message and exit
```

As you can see from the output, we need to pass the `chat_id` of the user who should receive code review messages. Replace 123456789 with your chat_id.<br>
Input:
```
python3 main.py 123456789
```

Output:
```
2023-09-14 15:38:13,868 - apscheduler.scheduler - INFO - Scheduler started
```

In order for the bot to send you messages, go into a dialog with it and click `start`.<br>
Once the code review on the lesson is ready, you will receive one of the following messages.

If there are edits:
```
У вас проверили урок "{lesson_title}"

К сожалению нашлись ошибки.
Для просмотра урока перейдите по ссылке: {lesson_url}
```

If there are no edits:
```
У вас проверили урок "{lesson_title}"

Преподавателю все понравилось. Можно приступать к следующему уроку!
Для просмотра урока перейдите по ссылке: {lesson_url}
```

Where instead of lesson_title and lesson_url will be the lesson title and lesson url from [dvmn.org](https://dvmn.org/).
