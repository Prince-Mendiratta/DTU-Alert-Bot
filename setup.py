import subprocess
import sys
import os.path
from os import path
######## This script is only for educational purpose ########
######## use it on your own RISK ########
######## I'm not responsible for any loss or damage ########
######## caused to you using this script ########
######## Github Repo - https://github.com/Dark-Princ3/DTU-Alert-Bot/ ########


def install(name):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', name])


def main():

    my_packages = ['Pyrogram', 'TgCrypto', 'psycopg2-binary', 'python-dotenv',
                   'lxml', 'bs4', 'requests', 'urllib3', 'pymongo', 'dnspython']

    env_vars = ['TG_BOT_TOKEN', 'API_ID',
                'API_HASH', 'AUTH_CHANNEL', 'MONGO_URL']

    for package in my_packages:
        install(package)
        print('\n')

    print("\n[*] Setting up Environment Variables. Please get the values ready.",
          "\n!!! Please read the repo's README for details on Enivronment variables.")

    if path.exists("config.env"):
        os.remove("config.env")

    fp = open('config.env', 'a+')

    for index, pr in enumerate(env_vars, start=1):
        print('\n[*] ' + str(index) + ' ' + pr)
        inpErr = True
        while inpErr != False:
            userInput = input()
            if not userInput:
                print("No input detected. Terminating.")
                sys.exit()
            else:
                var_key = env_vars[index - 1]
                var_value = userInput
                fp.write(var_key + '="{}"\n'.format(var_value))
                inpErr = False

    print('\n[*]Setup Completed! To add optional vars, copy from sample_config.env .')


if __name__ == '__main__':
    main()
