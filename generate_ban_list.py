# -*- coding: utf-8 -*-
import json
import os
import time
import requests
from retrying import retry
import configparser

conf = configparser.ConfigParser()

conf.read('mprdb.ini')
min_point_toban = float(conf.get('mprdb', 'min_point_toban'))
file_server_banlist = "banned-players.json"
file_reputation = "reputation.json"
source = conf.get('mprdb', 'ban_source')
expires = conf.get('mprdb', 'ban_expires')
reason = conf.get('mprdb', 'ban_reason')

# load old ban list and local reputation
with open(file_reputation, "r", encoding='utf-8') as f:
    reputation = json.loads(f.read())
with open(file_server_banlist, "r", encoding='utf-8') as d:
    banlist = json.loads(d.read())

already_exist_player = []  # Prevent duplication
for items in banlist:  # type(items)=dict
    already_exist_player.append(items["uuid"])

banamount = 0  # For progress bar
for player_uuid in reputation:
    if reputation[player_uuid] < min_point_toban:
        if player_uuid not in already_exist_player:
            banamount += 1
i = 1
# if a player in local reputation with a low point , and he isn't in the old ban list
# he will be add to the new ban list
for player_uuid in reputation:
    if reputation[player_uuid] < min_point_toban:
        if player_uuid not in already_exist_player:
            url = "https://sessionserver.mojang.com/session/minecraft/profile/" + player_uuid  # get player name
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
                print("Player: " + player_uuid + " not found! < "+str(i)+" / "+str(banamount)+" >")
                i += 1
                continue
            else:
                result = res.json()
                player_name = result["name"]
                print("Now adding player: " + player_name + " ,UUID: " + player_uuid + " to ban list. < "+str(i)+" / "+str(banamount)+" >")
                created = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + " +0800"
                info = {'uuid': player_uuid, 'name': player_name, 'created': created, 'source': source,
                        'expires': expires, 'reason': reason}
                # print(info)
                banlist.append(info)  # new ban list
                # print(banlist)
                i += 1

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
with open("banned-players.json", "w+", encoding='utf-8') as fp:
    fp.write(json.dumps(banlist, indent=4, ensure_ascii=False))
input("Press any key to exit.")
