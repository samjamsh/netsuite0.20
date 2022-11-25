import os, base64, sys

parameter=[] # waits input of 4 arguments,  username password ip-address mac-address
arguments = [x for x in sys.argv]
help = f'usage: python3 {sys.argv[0]} username password router-ip'

if len(arguments) != 4 :
    sys.exit(help)
else:
    parameter=[argument for argument in arguments]


username = parameter[1] # router username
password = parameter[2] # router password
userpass = username+':'+password
bytes = userpass.encode('ascii')
encode = base64.b64encode(bytes)
hashh = str(encode)
cookie = hashh[2:-1]
ip = parameter[3] # router ip

######################################################################################

request = f"curl 'http://{ip}/cgi?5' -H 'Accept: */*' -H 'Accept-Language: pt-BR,pt;q=0.9' -H 'Connection: keep-alive' -H 'Content-Type: text/plain' -H 'Cookie: Authorization=Basic {cookie}' -H 'Origin: {ip}' -H 'Referer: http://{ip}/mainFrame.htm' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42' --data-raw '[LAN_WLAN#0,0,0,0,0,0#0,0,0,0,0,0]0,18\r\nname\r\nStandard\r\nSSID\r\nRegulatoryDomain\r\nPossibleChannels\r\nRegulatoryDomain\r\nAutoChannelEnable\r\nChannel\r\nX_TP_Bandwidth\r\nEnable\r\nSSIDAdvertisementEnabled\r\nBeaconType\r\nBasicEncryptionModes\r\nWPAEncryptionModes\r\nIEEE11iEncryptionModes\r\nX_TP_Configuration_Modified\r\nWMMEnable\r\nX_TP_FragmentThreshold\r\n' --compressed --insecure"
response = os.popen(request).read()

if "SSID=" in response:
    listed_response = response.split()
    ssid = listed_response[3][len("SSID="):]
    print(f"network ssid: {ssid}")

else:
    print(f"Error: {response}")
