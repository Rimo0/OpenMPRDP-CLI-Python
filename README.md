# OpenMPRDB-CLI-Python

A Python based MPRDB client

API : https://openmprdb.org

Test server : https://test.openmprdb.org/


# Environment

Please do not use network proxy when running this client.

Python 3 or later


# Python components

1.requests

2.retrying

3.pandas

4.python-gnupg

or using `pip install -r requirements.txt`

# Function

● set the remote openmprdb server instance, automatically upload the public key registration and save its own UUID

● import / trust others' public keys, set / adjust the trust level and the score weight of the corresponding trust level

● submit player reputation score and save the submitted UUID

● withdraw (delete) the player reputation score and use the previously saved UUID

● collect reputation data according to trusted server UUID / public key keyID

● generate player reputation scores based on local trust data

● collect reputation data

● automatically update players whose reputation value is lower than a certain score to banlist

# How to use

1. Configure the environment.

2. Generate a pair of public and private keys with `key_management.py`.

3. Edit config file `mprdb.ini`

4. Each functional module is an independent file, which can be started as required.

# Workflow
### First to run
1. run `key_management.py` and command `init` to generate a key pair
2. run `key_management.py` and command `list` and copy your keyid
3. copy the `keyid` and paste it into the parameter `serverkeyid` in the `mprdb.ini` file
5. modify the parameter `banlist_path` in `mprdb.ini`.Change it into your server's ban list path.
6. modify the parameter `min_point_toban = 0` in `mprdb.ini`. This is to add players whose reputation score is lower than this number to the ban list,the default value is 0
7. then you need to register first. run `register.py` to register yourself

### Pull from other servers
1. run `get_all_server.py` to get a list of registered servers 
2. run `get_trust_public_key`.py to download the public key of the server you want to trust
3. run `update.py` to update ban list.
The old ban list will be saved in folder `backup`

### If occured some errors,try the following components.
1. run `pull_submits_from_trusted_servers.py` to get submissions from servers you trust
2. run `generate_reputation_list.py` to generate a local reputation database
3. run `generate_ban_list.py` to generate a new ban list


### Create / delete submit
1. run `new_submit.py` to create a new submit
all submits will be saved to file `submit.json`
2. run `delete_submit.py` to delete a submit

### Delete server (yourself)
1. run `delete_server.py` to delete the server yourself from the remote server
you need to re-register later

### Delete server (you trusted)
1. run `key_management.py` and command `list` to list all the keys
2. delete public key in `key_management.py` , use command `del` , with its key's `fingerprint`
3. delete public key in folder `TrustPublicKey` , with its `server uuid`

### Other functions
1. `get_submit_detail.py` It's used to get a detail of a submission , through its `submit uuid`
2. `get_submit_from_other_servers.py` It's used to get all submits from a specific server ,  through its `server uuid`
3. `key_management.py` Key management
4. `reputation.json` The local reputation base
5. `submit.json` The submits logs
6. `submit-others.json` The logs except submits,such as delete server
7. `weight.json` The local weight base
8. `players_map.json` Saved players uuid and name
9. `weight_management.py` Set weight for servers that have not been weighted
