import os, sys, base64
router_address = '192.168.0.1'
b64_hash = 'YWRtaW46YWRtaW4='

def program_inputs():

    usage = f"use: python3 {sys.argv[0]} router_ip router_username router_password"
    if len(sys.argv) == 1:
        sys.exit(usage)

    elif len(sys.argv) > 4:
        sys.exit(usage)

    else:
        router_IpAddress = sys.argv[1]
        router_Username = sys.argv[2]
        router_Password = sys.argv[3]
        return router_IpAddress, router_Username, router_Password

def request():
    try:
        http_request = f"curl 'http://{router_address}/cgi?6' -H 'Accept: */*' -H 'Accept-Language: pt-BR,pt;q=0.9' -H 'Connection: keep-alive' -H 'Content-Type: text/plain' -H 'Cookie: Authorization=Basic {b64_hash}' -H 'Origin: http://{router_address}' -H 'Referer: http://{router_address}/mainFrame.htm' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26' --data-raw '[LAN_WLAN_ASSOC_DEV#0,0,0,0,0,0#1,1,0,0,0,0]0,4\r\nAssociatedDeviceMACAddress\r\nX_TP_TotalPacketsSent\r\nX_TP_TotalPacketsReceived\r\nX_TP_HostName\r\n' --compressed --insecure"
        response = os.popen(http_request).read()
        #[error]0
        error_0 = response[len(response) - len("[error]0"):] == "[error]0"
        if error_0 is True:
            return response
        else:
            sys.exit("request unsuccessfully, try again later")

    except Exception as error:
        print(error)

def customize_infos(http_response):
    try:
        lines = []
        line = ''
        for char in http_response:
            if char == "\n":
                lines.append(line)
                line = ''
            else:
                line+= char
        return lines if len(lines) > 0 else exit("no value for lines")
    except Exception as error:
        print(error)

router_IpAddress, router_Username, router_Password = program_inputs()
def parameters_filter():

    if len(router_IpAddress) < 8 or len(router_IpAddress) > 16:
        sys.exit()
    elif len(router_Username) < 4:
        sys.exit()
    elif len(router_Password) < 4:
        sys.exit()
    else:
        pass


    credentials = router_Username + ':' + router_Password
    credential_bytes = credentials.encode('ascii')
    credential_base64_bytes = base64.b64encode(credential_bytes)
    credential_base64_hashString = str(credential_base64_bytes)
    credential = credential_base64_hashString[2:-1]
    return router_IpAddress, credential


router_address, b64_hash = parameters_filter() # cookie
response = request()
info_lines = customize_infos(response)

def prints_infos(info_lines):
    HostName = info_lines[-1]
    active_devices = info_lines.count(HostName)
    print(f"there's {active_devices} devices in activity")
    init = 0
    end = 5
    device_number = 0
    for info_line in range(active_devices):
        device_number += 1
        client_data = info_lines[init:end]
        init+=5
        end+=5
        client_info = client_data[1:4]

        client_mac = client_info[0]
        client_packet_sent = client_info[1]
        client_packet_received = client_info[2]

        client_mac_address = client_mac[len("associatedDeviceMACAddress="):]
        client_Packet_Sent = client_packet_sent[len("X_TP_TotalPacketsSent="):]
        client_Packet_Received = client_packet_received[len("X_TP_TotalPacketsReceived="):]

        client = f"{device_number}  Device MacAddress: {client_mac_address} TotalPacketsSent: {client_Packet_Sent} TotalPacketsReceived: {client_Packet_Received}"
        print(client)
        print("#"*35)

prints_infos(info_lines)
