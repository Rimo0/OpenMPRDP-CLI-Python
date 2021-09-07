# coding:utf-8
import json
import os
import time
import traceback
import pandas as pd
import requests
from retrying import retry
import configparser
import gnupg
import shutil

gpg = gnupg.GPG(gnupghome='./gnupg')
conf = configparser.ConfigParser()

if not os.path.exists('submit-others.json'):
    with open('submit-others.json','w+') as f:
        f.write('{}')

# load local server name and server uuid from local file
conf.read('mprdb.ini')
server_uuid = conf.get('mprdb', 'serveruuid')
server_name = conf.get('mprdb', 'servername')
print("Server UUID:" + server_uuid)


with open("submit.json", 'r') as load_f:
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

# os.system("del message.txt.asc")

# os.system("gpg -a --clearsign message.txt")
conf.read('mprdb.ini')
keyid = conf.get('mprdb', 'ServerKeyId')
passphrase=input('input passphrase: ')
# in windows ,a pop will rise to enter the passphrase,others will not.
with open('message.txt', 'rb') as f:
    status = gpg.sign_file(f, keyid=keyid, output='message.txt.asc',passphrase=passphrase)

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

commit={}
with open('submit-others.json','r',encoding='utf-8') as f:
    commit=json.loads(f.read())

# check status
status = res.get("status")
if status == "OK":
    submit_uuid = res.get("uuid")
    print("\nDeleted commit successfully! The UUID submitted this time is:")
    print(submit_uuid)
    eventtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    info = {'Type': "Delete server", 'ServerName': server_name, 'ServerUUID': server_uuid,
                            'Points withdrawn': load_dict[delete_uuid]["Points"],
                            'Original reason': load_dict[delete_uuid]["Comment"],
                            'Playername': load_dict[delete_uuid]["Name"], 'Timestamp': ticks, 'Time': eventtime,
                            'Reason for revocation': comment, 'SubmitUUID': submit_uuid}
    commit[submit_uuid]=info
    with open('submit-others.json','w+',encoding='utf-8') as fd:
        fd.write(json.dumps(commit, indent=4, ensure_ascii=False))

if status == "NG":
    print("Submit not found,or Unauthorized")

input("Press any key to exit")
