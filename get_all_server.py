# -*- coding: utf-8 -*-

import traceback
import pandas as pd
import requests
from retrying import retry

maxnum = "50"
url = "https://test.openmprdb.org/v1/server/list" + "?limit=" + maxnum

print("Getting servers list...")
print("The last " + maxnum + " servers will be displayed.")

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
# print json.loads('"%s"' %res) #typr(res)=dict

df = pd.DataFrame(res["servers"])
df1 = df.loc[:, ['id', 'key_id', 'server_name', 'uuid']]  # hide key "public_key" here, it's useless now
print(df1)

input("Press any key to exit")
