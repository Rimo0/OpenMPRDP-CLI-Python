import os

print('Pulling submits...')
try:
    os.system('python3 pull_submits_from_trusted_servers.py -m auto')
except:
    print('An error occured when pulling submits!')
    exit()

print('Generating reputation base...')
try:
    os.system('python3 generate_reputation_list.py -m auto')
except:
    print('An error occured when generating reputation base!')
    exit()

print('Generating ban list...')
try:
    os.system('python3 generate_ban_list.py -m auto')
except:
    print('An error occured when generating ban list!')
    exit()

print('Done.')