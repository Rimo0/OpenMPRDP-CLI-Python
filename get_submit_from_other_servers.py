# -*- coding: utf-8 -*-

import time
import traceback
import pandas as pd
import requests
from retrying import retry
import argparse

parser = argparse.ArgumentParser(description="get submit from server")
parser.add_argument('-u','--uuid', default="None")
args = parser.parse_args()
serverid = args.uuid
correct_input=True

# solve the 16 32 and 36 bits' server uuid
while True:
    if serverid == 'None' or correct_input==False:
        serverid = input("Input the server UUID or server key ID: ")
    # print(len("2512ab29a00e8686")) #16
    if len(serverid) == 16:
        url = "https://test.openmprdb.org/v1/submit/key/" + serverid
        break
    if len(serverid) == 32 or len(serverid) == 36:
        url = "https://test.openmprdb.org/v1/submit/server/" + serverid
        break
    else:
        print("Illegal input, please re-enter")
        correct_input==False

print("Input the number you want to view, in reverse order")
limitnum = input("No restrictions, just leave it blank :")
print("\n")
if limitnum != "":
    url = url + "?limit=" + limitnum

print("View submits after this time")
print("Input like this:20210811")
limittime = input("No restrictions, just leave it blank :")
print("\n")

dt = "20210811"
timeArray = time.strptime(dt, "%Y%m%d")
timestamp = str(int(time.mktime(timeArray)))
# print timestamp
if limittime != "":
    url = url + "?after=" + limittime

try:
    @retry(stop_max_attempt_number=3)
    def _parse_url(url):
        response = requests.get(url, timeout=5)
        return response
    response = _parse_url(url)
except:
    print("An error occurred")
    print(traceback.format_exc())
    input("Press any key to exit")
    exit()

res = response.json()
# print json.loads('"%s"' %res) #type(res)=dict

try:
    df1 = pd.DataFrame(res["submits"])
except:
    print("404 Not found")
    print("This server may not exist or may have been deleted.")
    print(res)
    input("Press any key to exit")
    exit()

print(df1)

input("Press any key to exit")
