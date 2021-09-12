# -*- coding: utf-8 -*-
import json
import traceback
import requests
from retrying import retry
import argparse

parser = argparse.ArgumentParser(description="get submit detail")
parser.add_argument('-u','--uuid', default="None")
args = parser.parse_args()
uuid = args.uuid

if uuid == 'None':
    uuid = input("Input the UUID of the submit you want to check:")
    skip_pause=False
else:
    skip_pause=True
url="https://test.openmprdb.org/v1/submit/uuid/"+uuid

try:
    @retry(stop_max_attempt_number=3)
    def _parse_url(url):
        response = requests.get(url,timeout=5)
        return response
except:
    print("An error occurred")
    print(traceback.format_exc())
    input("Press any key to exit")
    exit()
response = _parse_url(url)   
res = response.json()
print(json.loads('"%s"' % res))  # type(res)=dict

status=res.get("status")
if status == "NG":
    print("400 Bad Request or 404 Not found")
    print("This submission may not exist or may have been deleted.")
    
if skip_pause==False:
    input("Press any key to exit")
else:
    print('Finished!')