# -*- coding: utf-8 -*-
import json
import os
import time
import traceback
import requests
from retrying import retry
import configparser
import gnupg

gpg = gnupg.GPG(gnupghome='./gnupg')
conf = configparser.ConfigParser()

if not os.path.exists('message.txt'):
    with open('message.txt','w+') as f:
        f.write('')

player_uuid = ""
player_name = ""
conf.read('mprdb.ini')
server_uuid = conf.get('mprdb', 'serveruuid')
server_name = conf.get('mprdb', 'servername')
print("Server UUID:" + server_uuid)

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

# get player name from his uuid ,or conversely,uuid can be 32 or 36 bits
while True:
    string = input("Input the player's UUID or NAME:")
    print("Searching for player....")
    if len(string) == 36 or len(string) == 32:
        player_uuid = string
        url = "https://sessionserver.mojang.com/session/minecraft/profile/" + player_uuid
        try:
            @retry(stop_max_attempt_number=3)
            def _parse_url(url):
                res = requests.get(url)
                return res

            res = _parse_url(url)
        except:
            print("An error occurred while searching the player.Try again later.")
            exit()
        if res.text == "":
            print("Player not found!")
            continue
        else:
            result = res.json()
            player_name = result["name"]
            break
    else:
        player_name = string
        url = "https://playerdb.co/api/player/minecraft/" + player_name
        try:
            @retry(stop_max_attempt_number=3)
            def _parse_url(url):
                res = requests.get(url)
                return res


            res = _parse_url(url)
        except:
            print("An error occurred while searching the player.Try again later.")
            exit()
        result = res.json()
        if result["code"] == "player.found":
            player_uuid = result["data"]["player"]["id"]
            break
        else:
            print("Player not found!")
            continue

print("\r")
print("=====Confirm the player=====")
print("Player Name:" + player_name)
print("Player UUID:" + player_uuid)
input("Press any key to continue.")

comment = input("Input the comment:")
while True:
    points = input("Input the points:")
    points = int(points)
    if points < -1 or points > 1 or points == 0:
        print("Illegal input. Please enter a number between - 1 and 1 except 0")
    else:
        break
ticks = str(int(time.time()))
points = str(points)

print("\r")
print("=====Confirm your submit=====")
print("Server UUID:" + server_uuid)
print("Timestamp:" + ticks)
print("Player Name:" + player_name)
print("Player UUID:" + player_uuid)
print("Points:" + points)
print("Comment:" + comment)
input("Press any key to continue.")

# writing message

with open("message.txt", 'r+', encoding='utf-8') as f:
    f.truncate(0)
    f.write("uuid: " + server_uuid)
    f.write("\n")
    f.write("timestamp: " + ticks)
    f.write("\n")
    f.write("player_uuid: " + player_uuid)
    f.write("\n")
    f.write("points: " + points)
    f.write("\n")
    f.write("comment: " + comment)

# os.system("del message.txt.asc")
# os.system("gpg -a --clearsign message.txt")

conf.read('mprdb.ini')
keyid = conf.get('mprdb', 'ServerKeyId')
passphrase=input('input passphrase: ')
# in windows ,a pop will rise to enter the passphrase,others will not.
with open('message.txt', 'rb') as f:
    status = gpg.sign_file(f, keyid=keyid, output='message.txt.asc',passphrase=passphrase)

url = "https://test.openmprdb.org/v1/submit/new"
headers = {"Content-Type": "text/plain"}

with open("message.txt.asc", "r", encoding='utf-8') as f:
    data = f.read()
    data = data.encode('utf-8')
try:
    @retry(stop_max_attempt_number=3)
    def _parse_url(url, data, headers):
        response = requests.put(url, data=data, headers=headers, timeout=5)
        return response
except:
    print("An error occurred")
    print(traceback.format_exc())
    input("Press any key to exit")
    exit()
response = _parse_url(url, data, headers)

res = response.json()
print(json.loads('"%s"' % res))  # type(res)=dict

if not os.path.exists('submit.json'):
    with open('submit.json','w+') as f:
        f.write('{}')

commit={}
print(type(commit))

# check status
status = res.get("status")
if status == "OK":
    submit_uuid = res.get("uuid")
    print("\nSubmitted successfully! The UUID submitted this time is:")
    print(submit_uuid)
    eventtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    with open('submit.json','r',encoding='utf-8') as f:
        commit=json.loads(f.read())

    info = {'Name': player_name, 'PlayerUUID': player_uuid, 'Points': points, 'Timestamp': ticks, 'Time': eventtime,
         'Comment': comment, 'SubmitUUID': submit_uuid, 'ServerUUID': server_uuid}
    commit[submit_uuid]=info

    with open('submit.json','w+',encoding='utf-8') as fd:
        fd.write(json.dumps(commit, indent=4, ensure_ascii=False))

if status == "NG":
    print("400 Bad Request or 401 Unauthorized")

print("Finished! Exitting in 10 seconds...")
time.sleep(10)
