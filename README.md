# DTU Notice Alert Bot

Need to be informed of notices which are being uploaded on [DTU's official website](https://dtu.ac.in) but can't be bothered to keep checking the website regularly? Same. Thus, this bot is here to help you! Simply visit and check out [@DTUAlertBot](https://telegram.dog/DTUAlertBot) to get subscribed for notifications in case of an update on your phone itself! 

* Please make sure the bot is unmuted and telegram app is allowed to send notification for the bot to function as required!

* If you want to create your own bot with customised messages, commands and new functions, make sure to fork and star the repository. You can use the following methods to deploy the bot!


## License

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [LICENSE](./LICENSE) for more details.


## Demo RoBot

- [@DTUAlertBot](https://telegram.dog/DTUAlertBot)

- Simply Start the bot to get added to Alert List!


## Deploying your own

#### The Easiest Way [Heroku ONLY 👾]

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

* Make sure to read below what the configuration variables do.

#### The Legacy Way

- if you want to run this bot in your GNU/Linux System,
- `mv sample_config.env config.env`
- Edit the `config.env` with the appropriate values.
- Read below, to understand what the configuration variables does.
- Run `python3 -m bot`.

## ENVironment VARiables

#### Mandatory Environment Variables

* `TG_BOT_TOKEN`: Create a bot using [@BotFather](https://telegram.dog/BotFather), and get the Telegram API token.

* `APP_ID`,
* `API_HASH`: Get these two values from [my.telegram.org/apps](https://my.telegram.org/apps).

* `AUTH_CHANNEL`:
Go to [@Rose](https://telegram.dog/MissRose_bot), send /id in the chat to get this value.

* `MONGO_URL`: You can get this value by creating a cluster on [MongoDB](https://mongodb.com) and getting the connection url.

#### Optional Environment Variables

* `TG_BOT_WORKERS`: Number of workers to use. 4 is the recommended (and default) amount, but your experience may vary.
 __Note__ that going crazy with more workers won't necessarily speed up your bot, given the amount of sql data accesses, and the way python asynchronous calls work.

* `COMMM_AND_PRE_FIX`: The command prefix. Telegram, by default, recommeds the use of `/`, which is the default prefix. ~~Please don't change this unless you know what you're doing.~~

* `START_COMMAND`: The command to check if the bot is alive, or for users to start the robot.

* `START_OTHER_USERS_TEXT`: The message that your bot users would see on sending /start message.

* `ONLINE_CHECK_START_TEXT`: The message that the bot administrators can use to check if bot is online.

* `HELP_MEHH`: The message that bot users would see on sending /help message.

* `TZ`: Timezone to make sure time related functions work as required.

* `LOG_FILE_ZZGEVC`: The path to store log files.

## Credits, and Thanks to

* [Shrimadhav U K](https://telegram.dog/SpEcHiDe) for providing framework!
* [Dan Tès](https://telegram.dog/haskell) for his [Pyrogram Library](https://github.com/pyrogram/pyrogram)
