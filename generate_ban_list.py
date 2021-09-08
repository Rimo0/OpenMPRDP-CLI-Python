# -*- coding: utf-8 -*-
import json
import os
import time
import requests
import shutil
from retrying import retry
import configparser

if not os.path.exists('players_map.json'):
    with open('players_map.json', 'w+') as f:
        f.write('{}')

if not os.path.exists('banned-players.json'):
    with open('banned-players.json', 'w+') as f:
        f.write('[]')


def backup():
    # backup old ban list
    timepoint = str(time.strftime("%Y%m%d-%H%M%S", time.localtime()))
    if not os.path.exists("backup"):
        os.makedirs("backup")
    filename = "banned-players-backup-" + timepoint + ".json"
    os.rename('banned-players.json', filename)
    shutil.copy(filename, "backup/")
    os.rename(filename, 'banned-players.json')
    return 0


def players_map_get(player_uuid):  # uuid to name
    players_map = {}
    with open('players_map.json', 'r') as f:
        players_map = json.loads(f.read())
    player_name = players_map.get(player_uuid, '-1')
    return player_name


def players_map_save(player_uuid, player_name):  # save uuid and name to file
    players_map = {}
    with open('players_map.json', 'r') as f:
        players_map = json.loads(f.read())
    players_map[player_uuid] = player_name
    with open('players_map.json', 'w+') as d:
        d.write(json.dumps(players_map, indent=4, ensure_ascii=False))
    return 0


def new_list(i):
    # create new ban list
    with open("banned-players.json", "w+", encoding='utf-8') as fp:
        fp.write(json.dumps(banlist, indent=4, ensure_ascii=False))
    return 0


def search_online(player_uuid, i,changed):  # return (name or code,i)
    url = "https://sessionserver.mojang.com/session/minecraft/profile/" + \
        player_uuid  # get player name
    # print(url)
    try:
        @retry(stop_max_attempt_number=3)
        def _parse_url(url):
            res = requests.get(url)
            return res
        res = _parse_url(url)
    except:
        #print("An error occurred while searching the player.Try again later.")
        if changed:
            #print('Solved '+str(i)+' item<s>.')
            backup()
            new_list(i)
            return "-2", i
        else:
            #print('Nothing Changed.')
            return "-3", i

    if res.text == "":
        # print("Player: " + player_uuid + " not found! < " +
        # str(i)+" / "+str(banamount)+" >")
        i += 1
        return '-1', i
    else:
        result = res.json()
        player_name = result["name"]
    return player_name, i


conf = configparser.ConfigParser()
conf.read('mprdb.ini')
min_point_toban = float(conf.get('mprdb', 'min_point_toban'))
file_server_banlist = conf.get('mprdb','banlist_path')
file_reputation = "reputation.json"
source = conf.get('mprdb', 'ban_source')
expires = conf.get('mprdb', 'ban_expires')
reason = conf.get('mprdb', 'ban_reason')
changed = False

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
    if reputation[player_uuid] <= min_point_toban:
        if player_uuid not in already_exist_player:
            banamount += 1
i = 0
# if a player in local reputation with a low point , and he isn't in the old ban list
# he will be add to the new ban list
for player_uuid in reputation:
    if reputation[player_uuid] <= min_point_toban and player_uuid not in already_exist_player:
        if players_map_get(player_uuid) != '-1':
            player_name = players_map_get(player_uuid)
            i += 1
        else:
            player_name, i = search_online(player_uuid, i,changed)
            if player_name == '-3':
                print("An error occurred while searching the player.Try again later.")
                print('Nothing changed.')
                exit()
            if player_name == '-2':
                print("An error occurred while searching the player.Try again later.")
                print('Solved '+str(i)+' item<s>.')
                exit()
            if player_name == '-1':
                print("Player: " + player_uuid + " not found! < " +
                      str(i)+" / "+str(banamount)+" >")
                continue
            players_map_save(player_uuid,player_name)
            i += 1

        print("Now adding player: " + player_name + " ,UUID: " +
              player_uuid + " to ban list. < "+str(i)+" / "+str(banamount)+" >")
        created = str(time.strftime("%Y-%m-%d %H:%M:%S",
                                    time.localtime())) + " +0800"
        info = {'uuid': player_uuid, 'name': player_name, 'created': created, 'source': source,
                'expires': expires, 'reason': reason}
        # print(info)
        banlist.append(info)  # new ban list
        # print(banlist)
        changed = True

if changed:
    print('Solved '+str(i)+' item<s>.')
    backup()
    new_list(i)
else:
    print('Nothing changed.')

input("Press any key to exit.")
