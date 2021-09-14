# -*- coding: utf-8 -*-
import os
import traceback
import requests
from retrying import retry
import configparser
import gnupg
import shutil
import json
import time
import argparse

parser = argparse.ArgumentParser(description='get trust public key')
parser.add_argument('-u','--uuid',default='')
parser.add_argument('-w','--weight',default='-1')
parser.add_argument('-c','--choice',default='-1')
args = parser.parse_args()
serverid = args_uuid = args.uuid
point = float(args.weight)
args_choice = args.choice

def weight(server_uuid,point):
    if not os.path.exists('weight.json'):
    	with open('weight.json','w+') as f:
        	f.write('{}')

    with open("weight.json",'r') as f:
        key_list=json.loads(f.read())

    key_list[server_uuid]=point
    
    with open("weight.json", "w") as fp:
        fp.write(json.dumps(key_list,indent=4))
    return 0

if not os.path.exists('TrustPublicKey'):
    os.mkdir('TrustPublicKey')

gpg = gnupg.GPG(gnupghome='./gnupg')
conf = configparser.ConfigParser()

maxnum = "50"
url = "https://test.openmprdb.org/v1/server/list" + "?limit=" + maxnum

try:
    @retry(stop_max_attempt_number=3)
    def _parse_url(url):
        response = requests.get(url, timeout=5)
        return response
except:
    print("An error occurred")
    print(traceback.format_exc())
    input("Press any key to exit")
    exit()
response = _parse_url(url)
res = response.json()
# print json.loads('"%s"' %res) #type(res)=dict

# create some dicts , to match data
uuid_dict = {}  # dict "uuid":"public_key"
for items in res["servers"]:
    uuid = str(items["uuid"])
    public_key = str(items["public_key"])
    uuid_dict[uuid] = public_key

keyid_dict = {}  # dict "key_id":"public_key"
for items in res["servers"]:
    keyid = str(items["key_id"])
    public_key = str(items["public_key"])
    keyid_dict[keyid] = public_key

uuid_name_dict = {}  # dict "uuid":"name"
for items in res["servers"]:
    uuid = str(items["uuid"])
    name = str(items["server_name"])
    uuid_name_dict[uuid] = name

keyid_name_dict = {}  # dict "key_id":"name"
for items in res["servers"]:
    keyid = str(items["key_id"])
    name = str(items["server_name"])
    keyid_name_dict[keyid] = name

keyid_uuid_dict = {}  # dict "key_id":"uuid"
for items in res["servers"]:
    keyid = str(items["key_id"])
    uuid = str(items["uuid"])
    keyid_uuid_dict[keyid] = uuid

correct_input = True

# get server uuid from server name, or conversely
while True:
    while True:
        # i = os.system("cls")
        if correct_input == False:
            print('Command 0 to exit.')
            serverid = input("Input the server FULL UUID or server key ID: ")
        # print(len("2512ab29a00e8686")) #16
        if serverid == '':
            correct_input=False
            continue
        if serverid == '0':
            exit()
        if len(serverid) == 16:
            server_name = keyid_name_dict[serverid]
            server_uuid = keyid_uuid_dict[serverid]
            break
        if len(serverid) == 36:
            server_name = uuid_name_dict[serverid]
            server_uuid = serverid
            break
        else:
            correct_input = False
            print("Illegal input, please re-enter")

    print("\r")
    print("=====Confirm the server to trust=====")
    print("Server Name:" + server_name)
    print("Server UUID:" + server_uuid)
    print("Server key_id:" + serverid)
    print("Public key block:\n")
    print(uuid_dict[server_uuid])
    print("\r")

    choice = args_choice
    while True:
        if int(choice) < 0 or int(choice) > 4:
            print('Input 1 to save and import this public key, 2 to re-enter')
            print("3 to only save this public key, 0 to exit")
            choice = input("Input a number :")
        else:
            break

    file_name = server_uuid
    if choice == "1":
        with open(file_name, 'w') as f:
            f.write(uuid_dict[server_uuid])
        try:
            shutil.move(server_uuid,"TrustPublicKey")
        except:
            print('Already saved.')
            os.remove(server_uuid)
        # command = "move " + server_uuid + " %cd%\\TrustPublicKey"  # move key file
        # os.system(command)


        filepath = "./TrustPublicKey/" + server_uuid  # import key file
        key_data = open(filepath).read()
        import_result = gpg.import_keys(key_data)
        print(import_result.results)

        correct_input = True
        while True:
            if correct_input == False:
                point=float(input("Input the weight,from 0 to 5,except 0 :"))
            
            if point < 0 and correct_input == True: # default = -1
                correct_input=False
                continue

            if point>5 or point<=0:
                print("Illegal input, please re-enter,from 0 - 5")
                continue
            break
        weight(server_uuid,point)
        if args_uuid != '': # break in command line
            break

    if choice == "3":
        with open(file_name, 'w') as f:
            f.write(uuid_dict[server_uuid])
        if args_uuid != '': # break in command line
            break
    if choice == "0":
    	break

if args_uuid == '': 
    print("Finished! Exitting in 5 seconds...")
    time.sleep(5)
else: # skip pause in command line
    print('Done!')