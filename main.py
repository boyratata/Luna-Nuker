import sys
import json
import string
import random
from os import system
from random import randint
from itertools import cycle
from time import time, sleep
from threading import Thread
from pypresence import Presence
from requests_futures.sessions import FuturesSession

version = "1.0"

session = FuturesSession()
user_ids = []
role_ids = []
channel_ids = []
proxies = []
rotating = cycle(proxies)

if sys.platform == "linux":
    clear = lambda: system("clear")
else:
    clear = lambda: system("cls & mode 80,24")

clear()
print('''
     \x1b[38;5;199m    __                     
        / /   __  ______  ____ _
       / /   / / / / __ \/ __ `/
      / /___/ /_/ / / / / /_/ / 
     /_____/\__,_/_/ /_/\__,_/  \x1b[0mBETA\x1b[0m
''')

try:
    for line in open('Proxies.txt'):
        proxies.append(line.replace('\n', ''))
except Exception as e:
    print(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mFailed To Load Proxies From Proxies.txt. Error: {e}")

with open('Config.json') as f:
    config = json.load(f)

Token = config.get('Token')
Bot = config.get('Bot')
headers = {"Authorization": f"Bot {Token}"} if Bot else {"Authorization": f"{Token}"}

class LunaMisc:
    @staticmethod
    def Check(token, bot):
        headers = {"Authorization": f"Bot {token}"} if bot else {"Authorization": f"{token}"}
        r = session.get("https://discord.com/api/v8/users/@me", headers=headers).result()
        return r.status_code == 200

    @staticmethod
    def Ban(guild_id, member_id):
        try:
            r = session.put(f"https://discord.com/api/v{randint(6, 8)}/guilds/{guild_id}/bans/{member_id}", headers=headers, proxies={"http": 'http://' + next(rotating)}).result()
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                print(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mSuccessfully Banned {member_id}")
            elif r.status_code == 429:
                print("     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mRate limited. Retrying...")
                sleep(2)  # Add a short delay before retrying
                LunaMisc.Ban(guild_id, member_id)  # Retry logic
        except Exception as e:
            print(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mError: {e}")

    @staticmethod
    def Unban(guild_id, member_id):
        try:
            r = session.delete(f"https://discord.com/api/v{randint(6, 8)}/guilds/{guild_id}/bans/{member_id}", headers=headers, proxies={"http": 'http://' + next(rotating)}).result()
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                print(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mSuccessfully Unbanned {member_id}")
            elif r.status_code == 429:
                print("     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mRate limited. Retrying...")
                sleep(2)
                LunaMisc.Unban(guild_id, member_id)
        except Exception as e:
            print(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mError: {e}")

    @staticmethod
    def Kick(guild_id, member_id):
        try:
            r = session.put(f"https://discord.com/api/v{randint(6, 8)}/guilds/{guild_id}/members/{member_id}", headers=headers, proxies={"http": 'http://' + next(rotating)}).result()
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                print(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mSuccessfully Kicked {member_id}")
            elif r.status_code == 429:
                print("     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mRate limited. Retrying...")
                sleep(2)
                LunaMisc.Kick(guild_id, member_id)
        except Exception as e:
            print(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mError: {e}")

# Add other functions following the same pattern as needed

def Init():
    if LunaMisc.Check(Token, Bot):
        print(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mAuthenticated Token!")
        guild = input(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mGuild\x1b[38;5;199m: \x1b[0m")

        try:
            members = open('Scraped/Members.txt').readlines()
            user_ids.extend(member.strip() for member in members)
            roles = open('Scraped/Roles.txt').readlines()
            role_ids.extend(role.strip() for role in roles)
            channels = open('Scraped/Channels.txt').readlines()
            channel_ids.extend(channel.strip() for channel in channels)
        except Exception as e:
            print(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mFailed To Load Scraped Data! Error: {e}")

        print(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mLoaded {len(user_ids)} Members!")
        print(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mLoaded {len(role_ids)} Roles!")
        print(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mLoaded {len(channel_ids)} Channels!")
        sleep(2)
        Menu(guild)
    else:
        print(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mInvalid Token!")
        input()
        exit()

def Menu(guild):
    try:
        clear()
        print('''
     \x1b[38;5;199m    __                     
        / /   __  ______  ____ _ 
       / /   / / / / __ \/ __ `/ 
      / /___/ /_/ / / / / /_/ / 
     /_____/\__,_/_/ /_/\__,_/  \x1b[0mBETA\x1b[0m
    ''')
        print(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mGuild\x1b[38;5;199m: \x1b[0m{guild}")
        print(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mPlease Select An Option!")
        print(f"     \x1b[38;5;199m[\x1b[0m1\x1b[38;5;199m] \x1b[0mBan Members")
        print(f"     \x1b[38;5;199m[\x1b[0m2\x1b[38;5;199m] \x1b[0mUnban Members")
        print(f"     \x1b[38;5;199m[\x1b[0m3\x1b[38;5;199m] \x1b[0mKick Members")
        print(f"     \x1b[38;5;199m[\x1b[0m4\x1b[38;5;199m] \x1b[0mExit")
        choice = input(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mChoice\x1b[38;5;199m: \x1b[0m")

        if choice == "1":
            guild_id = input(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mEnter Guild ID\x1b[38;5;199m: \x1b[0m")
            member_id = input(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mEnter Member ID\x1b[38;5;199m: \x1b[0m")
            LunaMisc.Ban(guild_id, member_id)
        elif choice == "2":
            guild_id = input(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mEnter Guild ID\x1b[38;5;199m: \x1b[0m")
            member_id = input(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mEnter Member ID\x1b[38;5;199m: \x1b[0m")
            LunaMisc.Unban(guild_id, member_id)
        elif choice == "3":
            guild_id = input(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mEnter Guild ID\x1b[38;5;199m: \x1b[0m")
            member_id = input(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mEnter Member ID\x1b[38;5;199m: \x1b[0m")
            LunaMisc.Kick(guild_id, member_id)
        elif choice == "4":
            print("Exiting...")
            exit()
        else:
            print("Invalid Option! Please try again.")
            sleep(2)
            Menu(guild)
    except Exception as e:
        print(f"     \x1b[38;5;199m[\x1b[0m~\x1b[38;5;199m] \x1b[0mError: {e}")
        sleep(2)
        Menu(guild)

if __name__ == "__main__":
    Init()
