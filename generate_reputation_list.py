# -*- coding: utf-8 -*-
import os
import json
import time

start = time.time()
count = 0

reputation = {}

# load weight file
with open("weight.json", 'r') as f:
    weight = json.loads(f.read())

file_dir = "TrustPlayersList"
server_list = os.listdir(file_dir)  # server list

for server in server_list:
    submit_list = os.listdir(file_dir + "/" + server)  # submit list

    if weight.get(server) is None:
        print("Server :" + server + " has no weight set.")
        input("Press any key to exit")
        exit()
    else:
        pownum = float(weight.get(server))  # The weight of each trusted server is different

    for submit in submit_list:
        submit_dir = file_dir + "/" + server + "/" + submit
        with open(submit_dir, 'r', encoding='utf-8') as f:
            content = f.read()
        uuid_index = content.find("player_uuid:")
        if content[uuid_index + 12] == " ":  # with space
            player_uuid = content[uuid_index + 13:uuid_index + 49]
        if content[uuid_index + 12] != " ":  # without space
            player_uuid = content[uuid_index + 12:uuid_index + 48]
        point_index = content.find("points:")
        if content[point_index + 7] == " ":  # with space
            i = 0
            while True:  # get point number,accept decimals
                i += 1
                point_end_index = point_index + 7 + i
                if content[point_end_index] == "." or content[point_end_index] == "-":
                    continue
                try:
                    int(content[point_end_index])
                except:
                    break
            player_point_ori: float = float(content[point_index + 8:point_end_index]) # point before being weighted
            player_point = float(content[point_index + 8:point_end_index]) * pownum # point after being weighted
        if content[point_index + 7] != " ":  # without space
            i = 0
            while True:  # get point number,accept decimals
                i += 1
                point_end_index = point_index + 6 + i
                if content[point_end_index] == "." or content[point_end_index] == "-":  # Handle decimal points and minus signs
                    continue
                try:
                    int(content[point_end_index])
                except:
                    break
            player_point_ori = float(content[point_index + 7:point_end_index])
            player_point = float(content[point_index + 7:point_end_index]) * pownum
            # print(player_point)

        # If the player is not in the local reputation library, create a new record.
        # If it is, add it to the original value.
        if reputation.get(player_uuid) is None:
            reputation[player_uuid] = player_point
            sump = player_point
        else:
            sump = reputation[player_uuid]
            sump = sump + player_point
            reputation[player_uuid] = sump

        print("Solving player: " + player_uuid)
        print("With points: " + str(player_point_ori) + ", Magnification: " + str(pownum) + "x, Total points: " + str(
            sump))
        print("\n")
        count += 1

with open("reputation.json", "w+") as fp:
    fp.write(json.dumps(reputation, indent=4))

end = time.time()
print("=====================")
print("Solved " + str(count) + " submit<s>.")
print("Total time: " + str(end - start) + " second<s>.")
print("=====================")
print("Finished! Exitting in 3 seconds...")
time.sleep(3)
