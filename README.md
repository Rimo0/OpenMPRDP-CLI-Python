# OpenMPRDP-CLI-Python

A Python based MPRDB client

API : https://openmprdb.org

Test server : https://test.openmprdb.org/


# Environment

Python 3.7

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

3. Each functional module is an independent file, which can be started as required.

4. That's all.
