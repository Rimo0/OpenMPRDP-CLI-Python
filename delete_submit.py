# coding:utf-8
import json
import os
import time
import traceback
import pandas as pd
import requests
from retrying import retry

# load local server name and server uuid from local file
server_uuid = ""
count = 0
for line in open("server_uuid.txt"):
    count += 1
    if count == 1:
        server_name = line
    if count == 2:
        server_uuid = line
        break
print("Server UUID:" + server_uuid)

# standardize json
# add a { in the first line , remove the last line and add }} to it , to create a standard json
os.system("copy submit.json temp.json /y")
with open("temp.json", 'r+') as f:
    f.write("{")
with open("temp.json", "rb+") as f:
    lines = f.readlines()
    last_line = lines[-1]
    for i in range(len(last_line) + 2):
        f.seek(-1, os.SEEK_END)
        f.truncate()
with open('temp.json', 'a+') as f:  # temp.json is a standardized json from submit.json
    f.write("\n}}")

with open("temp.json", 'r') as load_f:
    load_dict = json.load(load_f)  # get ready to update the submit log
    # print(load_dict)

while True:
    delete_uuid = input("Input the UUID of the submit you want to delete:")
    if load_dict.get(delete_uuid):
        break
    else:
        print("Commit not found,please re-enter.")
        continue

print("\r")
print("=====Confirm the submit you want to delete=====")
print("Server UUID:" + server_uuid)
print("Server name:" + server_name)
df = pd.DataFrame.from_dict(load_dict[delete_uuid], orient='index')
print(df)
input("Press any key to continue.")
comment = input("Input the reason you delete the commit:")

# writing message
ticks = str(int(time.time()))
with open("message.txt", 'r+') as f:
    f.truncate(0)
    f.write("timestamp: " + ticks)
    f.write("\n")
    f.write("comment: " + comment)

os.system("del message.txt.asc")
os.system("gpg -a --clearsign message.txt")

url = "https://test.openmprdb.org/v1/submit/uuid/" + delete_uuid
headers = {"Content-Type": "text/plain"}

with open("message.txt.asc", "r") as f:
    data = f.read()

try:
    @retry(stop_max_attempt_number=3)
    def _parse_url(url, data, headers):
        response = requests.delete(url, data=data, headers=headers, timeout=5)
        return response
except:
    print("An error occurred")
    print(traceback.format_exc())
    input("Press any key to exit")
    exit()

response = _parse_url(url, data, headers)
res = response.json()
print(json.loads('"%s"' % res))  # type(res)=dict

# check status
status = res.get("status")
if status == "OK":
    submit_uuid = res.get("uuid")
    print("\nDeleted commit successfully! The UUID submitted this time is:")
    print(submit_uuid)
    eventtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open('submit-others.json', 'a') as f:
        f.write("\n")
        f.write("\"")
        f.write(submit_uuid)
        f.write("\":")
        f.write(json.dumps({'Type': "Delete server", 'ServerName': server_name, 'ServerUUID': server_uuid,
                            'Points withdrawn': load_dict[delete_uuid]["Points"],
                            'Original reason': load_dict[delete_uuid]["Comment"],
                            'Playername': load_dict[delete_uuid]["Name"], 'Timestamp': ticks, 'Time': eventtime,
                            'Reason for revocation': comment, 'SubmitUUID': submit_uuid}, sort_keys=False, indent=4,
                           separators=(',', ': ')))
        f.write(",")
if status == "NG":
    print("Submit not found,or Unauthorized")
os.system("del temp.json")
input("Press any key to exit")
