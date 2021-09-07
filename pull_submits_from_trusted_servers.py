# -*- coding: utf-8 -*-
import os
import time
import traceback
import requests
from retrying import retry
import configparser
import gnupg
import shutil

if not os.path.exists('TrustPlayersList'):
    os.mkdir('TrustPlayersList')

gpg = gnupg.GPG(gnupghome='./gnupg')
conf = configparser.ConfigParser()

start = time.time()
count = 0
submit_count = 0
server_count = 0

file_dir = "TrustPublicKey"
key_list = os.listdir(file_dir)  # list
error_key = []
error_code = []
server_all_count = len(key_list)
error_submit = []
error_submit_server = []
error_submit_server_count = 0

# load the keys that prepared to pull
for key in key_list:
    server_error = False
    server_count += 1
    submit_count = 0
    print("=====================")
    print("Now loading server :" + key + " --<Server:" +
          str(server_count) + "/" + str(server_all_count) + ">")
    url = "https://test.openmprdb.org/v1/submit/server/" + key

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

    print("HTTP status code: " + str(response.status_code))
    if response.status_code >= 400:
        print("An error occurred. Please try again later.")
        print("This key may be no longer available. Skip...")
        error_key.append(key)
        error_code.append(response.status_code)
        continue

    res = response.json()
    submits = res["submits"]
    submit_all_count = len(submits)

    for items in submits:  # decrypt
        submit_count += 1
        submit_uuid = items["uuid"]
        server_uuid = items["server_uuid"]
        content = items["content"]
        print("Now solving submit: " + submit_uuid + " --<Submit:" + str(submit_count) + "/" + str(
            submit_all_count) + ">" + " --<Server:" + str(server_count) + "/" + str(server_all_count) + ">")
        with open("temp.txt", 'w+', encoding='utf-8') as f:
            f.write(content)

        # result = subprocess.check_output("gpg --decrypt temp.txt", shell=True, stderr=subprocess.STDOUT,
        # stdin=subprocess.PIPE)  # gpg shell's output can't be got completely
        verify = False
        with open('temp.txt', 'rb') as f:
            verified = gpg.verify_file(f)
        if not verified:
            verify = False
        else:
            verify = True

        if verify:
            print("Good Signature. Saving....")
            path_name = './TrustPlayersList/' + server_uuid
            if not os.path.exists(path_name):
                os.makedirs(path_name)
            try:
                os.rename('temp.txt', submit_uuid)
                shutil.move(submit_uuid, path_name)
            except:
                print("Already Saved.Skip..")
                os.remove(submit_uuid)
            count += 1
        else:
            print(str(submit_uuid) + " is not valid! skip...")
            error_submit.append(submit_uuid)
            error_submit_server.append(key)
            server_error = True
    if server_error:
        error_submit_server_count += 1
end = time.time()
print("\n")
print("=====================")
print("Pulled " + str(count) + " submit<s>.")
print("Total time: " + str(end - start) + " second<s>.")
print("=====================")

# print error servers
if len(error_key) >= 1:
    print("There was a problem pulling submissions from the following " +
          str(len(error_key)) + " server<s>")
    i = 0
    for items in error_key:
        print("Server UUID: " + str(items) +
              " ,HTTPcode=" + str(error_code[i]))
        i += 1
else:
    print("All servers responded correctly.")
print("=====================")

# print error submits
if len(error_submit) >= 1:
    print("There was a problem verifying the signatures of the following " + str(
        len(error_submit)) + " submit<s>,from " + str(error_submit_server_count) + " server<s>")
    i = 0
    # solving the foling i-1
    error_submit_server.append(error_submit_server[0])
    print("\n")
    print("  >> from server: " + error_submit_server[0])
    for items in error_submit:
        if error_submit_server[i] != error_submit_server[i - 1]:
            print("  >> from server: " + error_submit_server[i])
        print("Submit UUID: " + str(items))
        i += 1
else:
    print("All signatures have been verified well and saved.")
print("\n")
input("Finished! Press any key to exit.")
