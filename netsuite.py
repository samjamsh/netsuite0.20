# netsuite : a suite of network tools
# tplink managment tool : tool created to run in tplink router only
# version 1.0 of tplink mangment tool

options = ['1. see connected devices on network','2. see devices in (black) block list','3. add a device in block/black list','4. Block a device in network/ enable or disale a device in network','5. Change router credentials','6. see or change black/block list state and enable or disable','7. see sent and received packets on netowrk online devices','8. see network ssid','9. change network ssid']

info = 'with this tool you can do: see all devices connected into network, put any device in black/block list, block/ unblock devices in network, see all devices into black/block list, change administrator page credentials, enable or disable devices in black/block list, and see if lobk/black list in ON (enabled) or OFF (disabled), see packets number sent and received on active network connected devices, see network ssid name/ see current network name, change current network ssid name/ change network ssid'

import os, sys, socket, random

try:
    # prints tool options
    for option in options:
        print(option)

    print(info) # information about tool utilities
    action = input('choice a option: ')
    username = input('router user: ')
    password = input('router pass: ')
    router = input('router address: ')


except Exception as err:
    sys.exit(err)

except:
    sys.exit("Error: some error in user data input!")


# gets machine ip address
def router_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('tplinkwifi.net', 80))
        ip = s.getsockname()[0][:-2]
        s.close()
    except Exception as error:
        sys.exit(f"{error}! make sure that you're connected into a network")

    except:
        sys.exit("Error: some error taking ip address!")

    return ip


if len(username) < 2 and len(password) < 2 and len(router) < 2:
    username = 'admin' # default tplink credential
    password = 'admin' # default tplink credential
    router = router_ip()
else:
    pass

try:
    path = '' # a path (reserved to be used as an api) you can use it as your api to run this tool from /bin directory or another one
    if action == '1':
        # see connected devices
        os.system(f'python3 {path}connected.py {username} {password} {router}')

    elif action == '2':
        # see devices in block list
        os.system(f"python3 {path}black.py {username} {password} {router} n")
    elif action == '3':
        # add device on block list
        mac = input('macaddress: ')
        state = input('sate: ')
        description = input('description: ')
        if len(mac) < 12 and len(state) < 1 and len(description) < 1:
            state = '0'
            mac = input('mac is required: ')
            rand = random.randrange(1,1000)
            descri = random.randrange(rand)
            descript = random.randrange(1000,1500)+rand+descri
            description = str(rand)+'.'+'default'+str(descri)+'..'+str(descript)
            print(description)
        else:
            pass

        os.system(f"python3 {path}add.py  {username} {password} {router} {mac} {state} {description}")

    elif action == '4':
        # enable/disable a device
        id = input('device id: ')
        state = input('0.Disable/1.Enable: ')
        if state == 'enable' or state == '1':
            state = '1'
        elif state == 'disable' or state == '0':
            state = '0'
        else:
            print('invalid option, use enable or disable')


        os.system(f"python3 {path}enable.py {username} {password} {router} {id} {state}")

    elif action == '5':
        # change router credentials
        new_user = input('new router user: ')
        new_pass = input('new router pass: ')
        os.system(f"python3 {path}change.py {username} {password} {router} {new_user} {new_pass}")

    elif action =='6':
        # change black/block list state, enabled or disabled mode
        state = input('mode: 1.enable; 2.disable> ')
        os.system(f'python3 {path}status.py {router} {username} {password}')
        os.system(f'python3 {path}mode.py {router} {username} {password} {state}')


    elif action == '7':
        # see packets being sent and received on network connected devices
        os.system(f"python3 {path}wireless-s.py {router} {username} {password}")

    elif action == '8':
        # see actual network current ssid name
        os.system(f"python3 {path}ssidconfirm.py {username} {password} {router}")

    elif action == '9':
        # change current network ssid name
        ssid = input("new ssid: ")
        os.system(f"python3 {path}change_ssid.py {username} {password} {router} {ssid}")

    else:
        # invalid option
        sys.exit('opcao invalida! use: 1, 2, 3, 4, 5 ou 6.')

except Exception as error:
    sys.exit(error)

except:
    sys.exit("Error: some error in main code execution")
