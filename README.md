# OpenMPRDB-CLI-Python

A Python based MPRDB client

API : https://openmprdb.org

Test server : https://test.openmprdb.org/


# Environment

Using network proxy may cause some errors.

Python 3 or later


# Python components

1.requests

2.retrying

3.pandas

4.python-gnupg

install then manually or use `pip install -r requirements.txt`

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

5. You can open it directly or run it from the command line

# Workflow
### 0x00 First to run

#### In command line
1. Command `python3 mprdb.py --key -n YourName -e YourEmail -p Passphrase -c Choice` to generate a key pair,about the argument `Choice`,input 1 means that the passphrase will be saved and auto fill in the future,input 0 to skip this step.
2. Command `python3 mprdb.py --key -m list` to get the key list
3. Copy the `keyid` and paste it into the parameter `serverkeyid` in the `mprdb.ini` file
4. modify the parameter `banlist_path` in `mprdb.ini`.Change it into your server's ban list path.
5. modify the parameter `min_point_toban = 0` in `mprdb.ini`. This is to add players whose reputation score is lower than this number to the ban list,the default value is 0
6. Command `python3 mprdb.py --reg -n ServerName [-p Passphrase]` to register yourself

#### Run Directly
1. run `key_management.py` and command `init` to generate a key pair
2. run `key_management.py` and command `list` and copy your keyid
3. copy the `keyid` and paste it into the parameter `serverkeyid` in the `mprdb.ini` file
4. modify the parameter `banlist_path` in `mprdb.ini`.Change it into your server's ban list path.
5. modify the parameter `min_point_toban = 0` in `mprdb.ini`. This is to add players whose reputation score is lower than this number to the ban list,the default value is 0
6. then you need to register first. run `register.py` to register yourself

### 0x01 Pull from other servers
The old ban list will be saved in folder `backup`

#### In command line
1. Command `python3 mprdb.py --list [-max MaxItemsToGet]` to get the list of registered server.
2. Command `python3 mprdb.py --getkey -u ServerUUID -c Choice -w Weight`,about the `Choice`,if you input 1,the key will be saved and import,if you input 3,the key will only be saved as a key file in MPRDB folder , with its ServerUUID;about the `weight` ,it can be a number from 0 to 5 ,except 0.
3. Command `python3 mprdb.py --update` to update the ban list


#### Run Directly
1. run `get_all_server.py` to get a list of registered servers 
2. run `get_trust_public_key.py` to download the public key of the server you want to trust
3. run `update.py` to update ban list.

#### If occured some errors,try the following components.
1. run `pull_submits_from_trusted_servers.py` to get submissions from servers you trust
2. run `generate_reputation_list.py` to generate a local reputation database
3. run `generate_ban_list.py` to generate a new ban list

### 0x02 Create / delete submit
All submits will be saved to file `submit.json`

#### In command line
1. Command `python3 mprdb.py --new -n PlayerName/UUID -r Reason -s Score [-p Passphrase]` to put a new submit
2. Command `python3 mprdb.py --del -u SubmitUUID -r Reason [-p Passphrase]` to delete a submit

#### Run Directly
1. run `new_submit.py` to create a new submit
2. run `delete_submit.py` to delete a submit

### 0x03 Delete server (yourself)

#### In command line
1. Command `python3 mprdb.py --shut -r Reason [-p Passphrase]` to delete yourself from the remote server

#### Run Directly
1. run `delete_server.py` to delete the server yourself from the remote server

### 0x04 Delete server (you trusted)
1. run `key_management.py` and command `list` to list all the keys
2. delete public key in `key_management.py` , use command `del` , with its key's `fingerprint`
3. delete public key in folder `TrustPublicKey` , with its `server uuid`

### 0x05 Import public key manually
The public key must be registered in remote server.

1. copy the key file to OpenMPRDB folder
2. rename the key to `key.asc`
3. run `key_management.py` and command `im`
4. move `key.asc` to folder `TrustPublicKey` , rename it to its server's uuid
5. run `weight_management.py` to set weight for it
6. run `update.py` to update ban list

### 0x06 Other functions
1. `get_submit_detail.py` It's used to get a detail of a submission , through its `submit uuid`

Command line: `python3 mprdb.py --detail -u SubmitUUID`

2. `get_submit_from_other_servers.py` It's used to get all submits from a specific server ,  through its `server uuid`

Command line: `python3 mprdb.py --listfrom -u ServerUUID`

3. `key_management.py` Key management
4. `reputation.json` The local reputation base
5. `submit.json` The submits logs
6. `submit-others.json` The logs except submits,such as delete server
7. `weight.json` The local weight base
8. `players_map.json` Saved players uuid and name
9. `weight_management.py` Set weight for servers that have not been weighted

Command `python3 mprdb.py --setweight -u ServerUUID -w Weight` to set or change weight for a specific server

10. `mprdb.py` Control center of command line parameters.Use `python mprdb.py -h` to get detail.
