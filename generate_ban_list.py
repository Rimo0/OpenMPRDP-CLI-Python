# -*- coding: utf-8 -*-
import json
import os
import time
import requests
from retrying import retry

min_point_toban = 0
file_server_banlist = "banned-players.json"
file_reputation = "reputation.json"
source = "OpenMPRDB"
expires = "forever"
reason = "Bad reputation"

# load old ban list and local reputation
with open(file_reputation, "r", encoding='utf-8') as f:
    reputation = json.loads(f.read())
with open(file_server_banlist, "r", encoding='utf-8') as d:
    banlist = json.loads(d.read())

already_exist_player = []  # Prevent duplication
for items in banlist:  # type(items)=dict
    already_exist_player.append(items["uuid"])

# if a player in local reputation with a low point , and he isn't in the old ban list
# he will be add in to the new ban list later
for player_uuid in reputation:
    if reputation[player_uuid] < min_point_toban:
        if player_uuid not in already_exist_player:
            url = "https://sessionserver.mojang.com/session/minecraft/profile/" + player_uuid # get player name
            # print(url)
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
                print("Now adding player: " + player_name + " ,UUID: " + player_uuid + " to ban list.")
                created = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + " +0800"
                info = {'uuid': player_uuid, 'name': player_name, 'created': created, 'source': source,
                        'expires': expires, 'reason': reason}
                # print(info)
                banlist.append(info) # new ban list
                # print(banlist)

# backup old ban list
time = str(time.strftime("%Y%m%d-%H%M%S", time.localtime()))
if not os.path.exists("backup"):
    os.makedirs("backup")

filename = "banned-players-backup-" + time + ".json"
command = "ren banned-players.json " + filename
os.system(command)
command = "move " + filename + " ./backup/"
os.system(command)

# create new ban list
with open("banned-players.json", "w+") as fp:
    fp.write(json.dumps(banlist, indent=4))
input("Press any key to exit.")
