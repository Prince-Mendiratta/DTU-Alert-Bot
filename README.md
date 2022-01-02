# DTU Notice Alert Bot

Need to be informed of notices which are being uploaded on [Delhi Technological University(DTU) official website](https://dtu.ac.in) but can't be bothered to keep checking the website regularly? Same. Thus, this bot is here to help you! Simply visit and check out [@DTUAlertBot](https://telegram.dog/DTUAlertBot) on [Telegram](https://telegram.org/) to get subscribed for notifications in case of an update on your phone itself!

- Please make sure the bot is unmuted and telegram app is allowed to send notification for the bot to function as required!

- If you want to create your own bot with customised messages, commands and new functions, make sure to fork and star the repository. You can use the following methods to deploy the bot!

## DISCLAIMER

This project has been submitted as a part of Innovative Project Work for degree of BACHELOR OF TECHNOLOGY in COMPUTER SCIENCE AND ENGINEERING, Delhi Technological University, Delhi by Prince Mendiratta (me). Please do not use this project source code without proper citations or reference to avoid infringement of License. See the [LICENSE](./LICENSE) for more details.
For reference, I have attached the [Project Report](https://github.com/Prince-Mendiratta/DTU-Alert-Bot/blob/master/Project_Report.pdf) itself as well in case someone wants some inspiration.

## Workflow
Since this bot was made keeping in mind that it will be hosted on [Heroku](https://heroku.com/) mostly, the project follows a [multi threaded approach](https://www.ibm.com/docs/en/aix/7.1?topic=concepts-multithreaded-programming) to prevent Heroku [dyno idling](https://devcenter.heroku.com/articles/free-dyno-hours#dyno-sleeping).  
The main thread is responsible for handling user events and commands on the [Telegram bot](https://t.me/DTUAlertBot) and creating child sub threads for checking the website for notice updates.

- The program creates sub threads, separate from the broadcast / telegram handling to check the website for updates at a set interval, which is 20 seconds by default.
- Upon initalising, a [JSON](https://www.json.org/json-en.html) record is created consisting of the current top 20 notices on the site, under each tab (Latest News, Tenders etc.) and is saved.
- Every 20 seconds, the site monitoring thread creates a JSON record and compares it with the saved JSON record. If there are any changes, the latest notice is sent to the notification subscribers on Telegram.

### WhatsApp Integration
- Bots on WhatsApp aren't easy to maintain and establish. Especially once mass messaging is involved, WhatsApp is pretty quick to **ban** accounts. Thus, it simply isn't possible to create a WhatsApp bot that can privately message people about notice updates.  
- To overcome this, a few groups were created where people can get updates. This is the most feasable way to accomplish the purpose at the point this project was made.  
- So, is the WhatsApp bot a separate bot with it's own notice checking threads? No. Instead, I have added [Webhook](https://en.wikipedia.org/wiki/Webhook) integration to this project itself.
- In the monitoring thread itself, once any udpates are detected, a webhook event is sent to the WhatsApp bot, which then proceeds to send the alert to the groups in the broadcast list.

### Webhook Security Measures
If the notices are conveyed via webhooks, wouldn't it be a disaster if someone found out the webhook URL and hijack the bot, doing whatever they want?! To prevent such a situation from occuring I have added several preventive measures, some of which are as follows.  
- The webhook URL itself is to be defined using [environment variables](https://en.wikipedia.org/wiki/Environment_variable). No hard-coded URL is used so that bypasses a lot of potential threats.  
- Let's say somehow someone still managed to get the URL, then is the bot compromised? No. The webhook uses SHA1 encrypted signatures to verify if any event sent to it has been sent from the monitoring thread only. Any other calls to the webhooks are rejected before even being processed.  
- The secret key for SHA1 has to be defined using environment variables, on both servers / dynos where the the telegram bot and the webhook are hosted.  
- The webhook takes advantage of Heroku's SSL for HTTPS communication.
- No valuable data is returned from the webhook so the sessions for WhatsApp are safe.
- The webhook server runs in a [chroot-jail](https://docs.oracle.com/cd/E37670_01/E41138/html/ch24s05.html) which mitigates a lot of potential issues that could occur if the project was hosted on a VPS.

## Demo RoBot

- [@DTUAlertBot](https://telegram.dog/DTUAlertBot)

- Simply Start the bot to get added to Alert List!

## Deploying your own

#### The Easiest Way [Heroku ONLY 👾]

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

- Make sure to read below what the configuration variables do.

#### On an Android Device

- Check the Mandatory Environment Variables given below and get their values.
- Download [Termux](https://play.google.com/store/apps/details?id=com.termux&hl=en_IN&gl=US) application from Play Store.
- Open Termux and enter `termux-setup-storage`. Allow Storage permissions.
- Enter `pkg install python git libxml2 libxslt clang`.
- Enter `python3 -m venv venv`.
- Enter `. ./venv/bin/activate`.
- Enter `cd /sdcard`.
- Enter `git clone https://github.com/Dark-Princ3/DTU-Alert-Bot`.
- Enter `cd DTU-Alert-Bot`.
- Enter `python3 setup.py`.
- Enter the 'mandatory' environment variables as prompted.
- Once setup is done, enter `python3 -m bot`.
- To enter optional variables, copy the key from sample_config.env and paste in config.env.

#### The Legacy Way

- if you want to run this bot in your GNU/Linux System,
- `cd code_directory`
- Enter `python3 setup.py`
- Enter the 'mandatory' environment variables as prompted
- Once setup is done, enter `python3 -m bot`
- To enter optional variables, copy the key from sample_config.env and paste in config.env.

## ENVironment VARiables

#### Mandatory Environment Variables

- `TG_BOT_TOKEN`: Create a bot using [@BotFather](https://telegram.dog/BotFather), and get the Telegram API token.

- `APP_ID`,
- `API_HASH`: Get these two values from [my.telegram.org/apps](https://my.telegram.org/apps).

- `AUTH_CHANNEL`:
  Go to [@Rose](https://telegram.dog/MissRose_bot), send /id in the chat to get this value.

- `MONGO_URL`: You can get this value by creating a cluster on [MongoDB](https://mongodb.com) and getting the connection url.

* **Note** You MUST enter 0.0.0.0/0 in the allowed ip addresses range in your cluster.

#### Optional Environment Variables

- `TG_BOT_WORKERS`: Number of workers to use. 4 is the recommended (and default) amount, but your experience may vary.
  **Note** that going crazy with more workers won't necessarily speed up your bot, given the amount of sql data accesses, and the way python asynchronous calls work.

- `COMMM_AND_PRE_FIX`: The command prefix. Telegram, by default, recommeds the use of `/`, which is the default prefix. ~~Please don't change this unless you know what you're doing.~~

- `START_COMMAND`: The command to check if the bot is alive, or for users to start the robot.

- `START_OTHER_USERS_TEXT`: The message that your bot users would see on sending /start message.

- `ONLINE_CHECK_START_TEXT`: The message that the bot administrators can use to check if bot is online.

- `HELP_MEHH`: The message that bot users would see on sending /help message.

- `TZ`: Timezone to make sure time related functions work as required.

- `LOG_FILE_ZZGEVC`: The path to store log files.

- `REQUEST_INTERVAL`: Time interval between each check.

## License

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [LICENSE](./LICENSE) for more details.

## Credits, and Thanks to

- [Shrimadhav U K](https://telegram.dog/SpEcHiDe) for providing framework!
- [Dan Tès](https://telegram.dog/haskell) for his [Pyrogram Library](https://github.com/pyrogram/pyrogram)
