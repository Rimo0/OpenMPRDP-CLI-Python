# -*- coding: utf-8 -*-
import os
import json
import time

file_dir = "TrustPublicKey"
new_key_list=os.listdir(file_dir) 

if not os.path.exists('weight,json'):
    with open('weight.json','w+') as f:
        f.write('{}')

with open("weight.json",'r') as f:
    old_key_list=json.loads(f.read())

wait_to_weight_list=[]
for items in new_key_list:
    point=old_key_list.get(items)
    if point==None:
        wait_to_weight_list.append(items)
#print(wait_to_weight_list)

if len(wait_to_weight_list)==0:
    print("No more servers wait to weight.")
    input("Press any key to exit")
    exit()

for items in wait_to_weight_list:
    uuid=items
    print("Server UUID now is :"+uuid)
    
    while True:
        point=float(input("Input the weight,from 0 to 5,except 0 :"))
        if point>5 or point<=0:
            print("Illegal input, please re-enter")
            continue 
        break
    old_key_list[uuid]=point
    
with open("weight.json", "w") as fp:
    fp.write(json.dumps(old_key_list,indent=4))
print("Finisned")
print("Finished! Exitting in 5 seconds...")
time.sleep(5)