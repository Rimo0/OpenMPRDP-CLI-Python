# -*- coding: utf-8 -*-
import json
import os
import time
import traceback
import requests
from retrying import retry

print("Only servers with no submit could be deleted using API.")
server_uuid = ""
count = 0
for line in open("server_uuid.txt"):
    count += 1
    if count == 1:
        server_name: str = line
    if count == 2:
        server_uuid = line
        break
print("Server UUID:" + server_uuid)

comment = input("Input the comment to delete:")

print("\r")
print("=====Confirm to delete server=====")
print("Server UUID:" + server_uuid)
print("Server name:" + server_name)
print("Comment:" + comment)
input("Press any key to continue")

# writing message
ticks = str(int(time.time()))
with open("message.txt", 'r+') as f:
    f.truncate(0)
    f.write("timestamp: " + ticks)
    f.write("\n")
    f.write("comment: " + comment)

os.system("del message.txt.asc")
os.system("gpg -a --clearsign message.txt")

url = "https://test.openmprdb.org/v1/server/uuid/" + server_uuid
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
    print("\nDeleted server successfully! The UUID submitted this time is:")
    print(submit_uuid)
    eventtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open('submit-others.json', 'a') as f:
        f.write("\n")
        f.write("\"")
        f.write(submit_uuid)
        f.write("\":")
        f.write(json.dumps(
            {'Type': "Delete submit", 'ServerName': server_name, 'ServerUUID': server_uuid, 'Timestamp': ticks,
             'Time': eventtime, 'Comment': comment, 'SubmitUUID': submit_uuid}, sort_keys=False, indent=4,
            separators=(',', ': ')))
        f.write(",")
if status == "NG":
    print("Server not found,or Unauthorized")

input("Press any key to exit")
