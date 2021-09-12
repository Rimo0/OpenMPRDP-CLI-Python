# -*- coding: utf-8 -*-
import json
import os
import time
import traceback
import requests
from retrying import retry
import configparser
import gnupg
import argparse

parser = argparse.ArgumentParser(description="Delete server self")
parser.add_argument('-r','--reason', default='None')
parser.add_argument('-p','--passphrase', default='None')
args = parser.parse_args()
comment = args.reason
passphrase = args.passphrase

gpg = gnupg.GPG(gnupghome='./gnupg')
conf = configparser.ConfigParser()

if not os.path.exists('submit-others.json'):
    with open('submit-others.json','w+') as f:
        f.write('{}')

print("Only servers with no submit could be deleted using API.")

conf.read('mprdb.ini')
server_uuid = conf.get('mprdb', 'serveruuid')
server_name = conf.get('mprdb', 'servername')

print("Server UUID:" + server_uuid)

if comment == 'None':
    comment = input("Input the comment to delete:")
    skip_pause=False
else:
    skip_pause=True

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

# os.system("del message.txt.asc")

# os.system("gpg -a --clearsign message.txt")
conf.read('mprdb.ini')
keyid = conf.get('mprdb', 'ServerKeyId')
if conf.get('mprdb','save_passphrase')=='True':
    passphrase=conf.get('mprdb','passphrase')
elif passphrase != 'None':
    passphrase = args.passphrase
else:
    passphrase=input('input passphrase: ')
# in windows ,a pop will rise to enter the passphrase,others will not.
with open('message.txt', 'rb') as f:
    status = gpg.sign_file(f, keyid=keyid, output='message.txt.asc',passphrase=passphrase)

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

commit={}
with open('submit-others.json','r',encoding='utf-8') as f:
    commit=json.loads(f.read())

# check status
status = res.get("status")
if status == "OK":
    submit_uuid = res.get("uuid")
    print("\nDeleted server successfully! The UUID submitted this time is:")
    print(submit_uuid)
    eventtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
    info={'Type': "Delete submit", 'ServerName': server_name, 'ServerUUID': server_uuid, 'Timestamp': ticks,
             'Time': eventtime, 'Comment': comment, 'SubmitUUID': submit_uuid}
    commit[submit_uuid]=info
    with open('submit-others.json','w+',encoding='utf-8') as fd:
        fd.write(json.dumps(commit, indent=4, ensure_ascii=False))

if status == "NG":
    print("Server not found,or Unauthorized")

if skip_pause==False:
    print("Finished! Exitting in 5 seconds...")
    time.sleep(5)
else:
    print('Finished!')
