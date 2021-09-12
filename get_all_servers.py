# -*- coding: utf-8 -*-

import traceback
import pandas as pd
import requests
from retrying import retry
import argparse

parser = argparse.ArgumentParser(description="get server lists")
parser.add_argument('-m','--max', default=45)
args = parser.parse_args()
maxnum = str(args.max)

# print(type(maxnum))
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

url = "https://test.openmprdb.org/v1/server/list" + "?limit=" + maxnum

print("Getting servers list...")
print("The last " + maxnum + " servers will be displayed.")

if maxnum == '45':
    skip_pause=True

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
res = response.json()
# print json.loads('"%s"' %res) #type(res)=dict

df = pd.DataFrame(res["servers"])
df1 = df.loc[:, ['id', 'key_id', 'server_name', 'uuid']]  # hide key "public_key" here, it's useless now
print(df1)

if skip_pause==False:
    input("Press any key to exit")
else:
    print('Finished!')