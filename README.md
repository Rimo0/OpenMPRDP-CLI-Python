# OpenMPRDB-CLI-Python

A Python based MPRDB client

API : https://openmprdb.org

Test server : https://test.openmprdb.org/


# Environment

Python 3.9

GunPG Client

Windows

# Python components

1.requests

2.retry

3.pandas


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

2. Generate a pair of public and private keys with gunpg client.

3. Export public key to openmprdb home directory

4. Each functional module is an independent file, which can be started as required.

# Workflow
### Pull from other servers
1. run get_all_server.py to get a list of registered servers 
2. run get_trust_public_key.py to download the public key of the server you want to trust
3. run weight_management.py to set weights for trusted servers
4. run pull_submits_from_trusted_servers.py to get submissions from servers you trust
5. run generate_reputation_list.py to generate a local reputation database
6. copy the old ban list to the OpenMPRDB home directory
7. modify this parameter "min_point_toban = 0" in generate_ban_list.py. This is to add players whose reputation score is lower than this number to the ban list,the default value is 0
8. run generate_ban_list.py to generate a new ban list
9. old ban list will be saved in fold "backup"

### Create / delete submit
1. you need to register first. run register.py to register yourself
2. run new_submit.py to create a new submit
3. all submits will be saved to file "submit,json"
4. run delete_submit.py to delete a submit

### Delete server (yourself)
1. run delete_server.py to delete the server yourself from the remote server
2. you need to re-register later

### Delete server (you trusted)
1. delete public key in GunPG Client
2. delete public key in fold "TrustPublicKey"

### Other functions
1. get_submit_detail.py It's used to get a detail of a submission , through its submit uuid
2. get_submit_from_other_servers.py It's used to get all submits from a specific server ,  through its server uuid
3. reputation.json The local reputation base
4. submit.json The submits logs
5. submit-others.json The logs except submits,such as delete server
6. weight.json The local weight base
7. server_uuid.txt It saved your server's name and uuid
