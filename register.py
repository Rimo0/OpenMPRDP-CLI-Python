# -*- coding: utf-8 -*-
import json
import os
import traceback
import requests
from retrying import retry

import configparser
import gnupg

gpg = gnupg.GPG(gnupghome='./gnupg')
conf = configparser.ConfigParser()

linenum = 0
sigstr = []
keystr = []
sigfilename = "message.txt.asc"
keyfilename = "public_key.asc"

server_name = input("Input the server name:")
with open("message.txt", 'r+', encoding='utf-8') as f:
    f.truncate(0)
    f.write("server_name:" + server_name)

# os.system("ren *_public.asc public_key.asc")
# os.system("del message.txt.asc")

# os.system("gpg -a --clearsign message.txt")

conf.read('mprdb.ini')
passphrase=input('input passphrase: ')
# in windows ,a pop will rise to enter the passphrase,others will not.

keyid = conf.get('mprdb', 'ServerKeyId')
with open('message.txt', 'rb') as f:
    status = gpg.sign_file(f, keyid=keyid, output='message.txt.asc',passphrase=passphrase)
	
sigcount = 0
for line in open(sigfilename):
    sigcount += 1
# print(sigcount, end = '') #Number of sig file lines

keycount = 0
for line in open(keyfilename):
    keycount += 1
# print(keycount, end = '') #Number of key file lines

for line in open(sigfilename):
    line = line[:-1]  # delete"\n"
    sigstr.append(line)

for line in open(keyfilename):
    line = line[:-1]  # delete"\n"
    keystr.append(line)

signature = "-----BEGIN PGP SIGNATURE-----\n\n"
for num in range(6, sigcount - 2):
    signature = signature + sigstr[num]
signature = signature + "\n" + \
    sigstr[sigcount - 2] + "\n-----END PGP SIGNATURE-----"

message = "-----BEGIN PGP SIGNED MESSAGE-----\n"
message = message + sigstr[1] + "\n\n" + sigstr[3] + "\n" + signature
# print(message, end = '')


pubkey = "-----BEGIN PGP PUBLIC KEY BLOCK-----\n\n"
for num in range(2, keycount - 2):
    pubkey = pubkey + keystr[num]
pubkey = pubkey + "\n" + keystr[-2] + "\n-----END PGP PUBLIC KEY BLOCK-----"
# print(pubkey, end = '')


with open('register.json', 'w') as f:
    f.write(json.dumps({'message': message, 'public_key': pubkey},
            sort_keys=True, indent=2, separators=(',', ': ')))

data = json.dumps({'message': message, 'public_key': pubkey},
                  sort_keys=True, indent=2, separators=(',', ': '))
print(data)

url = "https://test.openmprdb.org/v1/server/register"
headers = {"Content-Type": "application/json"}

try:
    @retry(stop_max_attempt_number=3)
    def _parse_url(url, data, headers):
        response = requests.put(url, data=data, headers=headers, timeout=5)
        return response
except:
    print("An error occurred")
    print(traceback.format_exc())
    input("Press any key to exit")
    exit()

response = _parse_url(url, data, headers)
res = response.json()
print(json.loads('"%s"' % res))  # typr(res)=dict
# print(type(res))

# check status
status = res.get("status")
if status == "OK":
    uuid = res.get("uuid")
    print("\nRegistration succeeded! The UUID of the current device is:")
    print(uuid)
    conf.read('mprdb.ini')
    conf.set('mprdb', 'ServerName', server_name)
    conf.set('mprdb', 'ServerUUID', uuid)
    conf.write(open('mprdb.ini', 'w'))
if status == "NG":
    print("400 Bad Request")

input("Press any key to exit")
