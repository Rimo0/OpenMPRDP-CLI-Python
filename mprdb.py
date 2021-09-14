import argparse
import sys
import os
import json


def key_management():
    # Key management
    # argv = key
    # -n --name
    # -e --email
    # -p --passphrase
    # -c --choice
    # -m --mode

    arg_name = args.name
    arg_email = args.email
    arg_passphrase = args.passphrase
    arg_choice = str(args.choice)
    arg_mode = args.mode

    if arg_name != 'None' and arg_email != 'None' and arg_passphrase != 'None':
        command = 'python3 key_management.py -m auto -n '+arg_name+' -e '+arg_email+' -p '+arg_passphrase+' -c '+arg_choice
        os.system(command)
        return 'Done!'
    elif arg_mode == 'list':
        command = 'python3 key_management.py -m list'
        os.system(command)
        return 'Done!'
    else:
        info = 'Missing arguments : --name or --email or --passphrase or --choice'
        return info

def register():
    # Register argv
    # argv = reg
    # -n --name
    # -p --passphrase
    arg_name = args.name
    arg_passphrase = args.passphrase
    
    if arg_name=='None' :
        info = 'Missing parameter : --name '
        return info
    else:
        command = 'python3 register.py -n '+arg_name
        if arg_passphrase != '':
            command = command +' -p '+arg_passphrase
        os.system(command)
        return 'Done!'


def new_submit():
    # New submits
    # argv = new
    # -n --name
    # -r --reason
    # -s --score
    # -p --passphrase
    arg_name = args.name
    arg_reason = args.reason
    arg_score = args.score
    arg_passphrase = args.passphrase
    
    if arg_name=='None' or arg_reason == 'None' or arg_score == 'None':
        info = 'Missing parameter : --name or --reason or --score'
        return info
    else:
        command = 'python3 new_submit.py -n '+arg_name+' -r '+arg_reason+' -s '+arg_score
        if arg_passphrase != '':
            command = command +' -p '+arg_passphrase
        os.system(command)
        return 'Done!'

def delete_submit():
    # Delete submits
    # argv = del
    # -u --uuid
    # -r --reason
    # -p --passphrase
    arg_uuid = args.uuid
    arg_reason = args.reason
    arg_passphrase = args.passphrase
    if arg_uuid=='None' or arg_reason == 'None':
        info = 'Missing parameter : --reason or --uuid'
        return info
    else:
        command = 'python3 delete_submit.py -u '+arg_uuid+' -r '+arg_reason
        if arg_passphrase != '':
            command = command +' -p '+arg_passphrase
        os.system(command)
        return 'Done!'


def delete_server():
    # Delete server
    # argv = shut
    # -r --reason
    # -p --passphrase
    arg_reason = args.reason
    arg_passphrase = args.passphrase
    if arg_reason == 'None':
        info = 'Missing parameter : --reason'
        return info
    else:
        command = 'python3 delete_server.py'+' -r '+arg_reason
        if arg_passphrase != '':
            command = command +' -p '+arg_passphrase
        os.system(command)
        return 'Done!'


def list_all_servers():
    # List all servers
    # argv = list
    # -m --max
    arg_max = str(args.max)
    command = 'python3 get_all_servers.py'
    if arg_max != '':
        command = command + ' -m '+arg_max
    os.system(command)
    return 'Done!'


def get_submit_detail():
    # Get submit detail
    # argv = detail
    # -u --uuid
    arg_uuid = args.uuid
    if arg_uuid == 'None':
        info = 'Missing parameter : --uuid.'
        return info
    else:
        command = 'python3 get_submit_detail.py'+' -u '+arg_uuid
        os.system(command)
        return 'Done!'

def get_submit_from_server():
    # Get submit from server
    # argv = listfrom
    # -u --uuid
    arg_uuid = args.uuid
    if arg_uuid == 'None':
        info = 'Missing parameter : --uuid.'
        return info
    else:
        command = 'python3 get_submit_from_other_servers.py'+' -u '+arg_uuid
        os.system(command)
        return 'Done!'


def help_info():
    info = 'try -h to get help info'
    return info

def update():
    os.system('python3 update.py')
    return 'Done!'

def getkey():
    # Get trusted public key
    # argv = getkey
    # -u uuid
    # -w weight
    # -c choice
    args_uuid = args.uuid
    args_weight = args.weight
    args_choice = args.choice

    if args_uuid == 'None' or args_weight == 'None' or args_choice == 'None':
        info = 'Missng arguments : --uuid or --weight or --choice'
        return info
    else:
        command = 'python3 get_trust_public_key.py -u '+args_uuid+' -w '+args_weight+' -c '+args_choice
        os.system(command)

def setweight():
    # args = setweight
    # -u --uuid
    # -w --weight
    args_uuid = args.uuid
    args_weight = args.weight

    if not os.path.exists('weight.json'):
    	with open('weight.json','w+') as f:
        	f.write('{}')
    
    with open("weight.json",'r') as f:
        key_list=json.loads(f.read())

    key_list[args_uuid]=args_weight
    
    with open("weight.json", "w") as fp:
        fp.write(json.dumps(key_list,indent=4))
    
    info = 'Set server weight : '+args_uuid+' to '+args_weight
    return info

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="main")

    # register sub keys
    parser.add_argument('-u', '--uuid', default='None',help=argparse.SUPPRESS)
    parser.add_argument('--max', default='45',help=argparse.SUPPRESS)
    parser.add_argument('-n', '--name', default='None',help=argparse.SUPPRESS)
    parser.add_argument('-r', '--reason', default='None',help=argparse.SUPPRESS)
    parser.add_argument('-s', '--score', default='None',help=argparse.SUPPRESS)
    parser.add_argument('-p', '--passphrase', default='',help=argparse.SUPPRESS)
    parser.add_argument('-e', '--email', default='None',help=argparse.SUPPRESS)
    parser.add_argument('-c', '--choice', default='None',help=argparse.SUPPRESS)
    parser.add_argument('-m', '--mode', default='manual',help=argparse.SUPPRESS)
    parser.add_argument('-w', '--weight',default='None',help=argparse.SUPPRESS)

    # register main keys
    parser.add_argument('--key', action='store_true', default=False,help='>>Used to generate key pair and get lists.With key "-n name -e email -i choice -p passphrase".Choice input 1 to save and auto fill passphrase in the future,0 will not.To get a list of keys, use key "-m list"')
    parser.add_argument('--reg', action='store_true', default=False,help='>>Used to register to a remote server.With key "-n server_name",and optional key "-p passphrase"')
    parser.add_argument('--new', action='store_true', default=False,help='>>Used to submit a new submission.With key "-n player_name/uuid -r reason -s score",and optional key "-p passphrase"')
    parser.add_argument('--delete', action='store_true', default=False,help='>>Used to delete a submission that have submitted.With key “-u submit_uuid -r reason”,and optional key "-p passphrase"')
    parser.add_argument('--shut', action='store_true', default=False,help='>>Used to delete yourself from the remote server.With key "-r reason",and optional key "-p passphrase"')
    parser.add_argument('--list', action='store_true', default=False,help='>>Used to get all registered servers.With an optional key "--max number",it means how many servers to list.')
    parser.add_argument('--detail', action='store_true', default=False,help='>>Used to get a detail of a submission.With key "-u submit_uuid"')
    parser.add_argument('--listfrom', action='store_true', default=False,help='>>Used to get all submission from a specific server.With key "-u server_uuid"')
    parser.add_argument('--update', action='store_true', default=False,help='>>Used to auto update the ban list.No key required.')
    parser.add_argument('--getkey',action='store_true',default=False)
    parser.add_argument('--setweight',action='store_true',default=False)

    args = parser.parse_args()

    if args.key == True:
        info = key_management()
        print(info)
    elif args.reg == True:
        info = register()
        print(info)
    elif args.new == True:
        info = new_submit()
        print(info)
    elif args.delete == True:
        info = delete_submit()
        print(info)
    elif args.shut == True:
        info = delete_server()
        print(info)
    elif args.list == True:
        list_all_servers()
    elif args.detail == True:
        info = get_submit_detail()
        print(info)
    elif args.listfrom == True:
        info = get_submit_from_server()
        print(info)
    elif args.update == True:
        update()
    elif args.getkey == True:
        info = getkey()
        print(info)
    elif args.setweight == True:
       info = setweight()
       print(info)
    else:
        print('Invalid parameter.')
        help_info()
