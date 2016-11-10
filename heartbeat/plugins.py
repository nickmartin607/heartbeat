def ping(host):
    from scapy.all import IP, ICMP, sr1
    try:
        packet = IP(dst=host.ip)/ICMP()
        result = sr1(packet, timeout=3)
        if result:
            return (True, 'Ping Succeeded - Host is Alive')
        else:
            return (False, 'Ping Succeeded - Host is Down')
    except Exception as e:
        return (False, 'Ping Failed - Error: "{}"'.format(e))

def port_connect(service=None, ip=None, port=None, timeout=5):
    from scapy.all import IP, TCP, sr1
    try:
        ip = service.host.ip if service else ip
        port = port or service.port
        packet = IP(dst=ip)/TCP(dport=port, flags='S', seq=1000)
        result = sr1(packet, timeout=3)
        if result:
            return (True, 'Port {} Connection Succeeded'.format(port))
        else:
            return (False, 'Port {} Connection Failed'.format(port))
    except Exception as e:
        return (False, 'Port Connection Failure - Error: "{}"'.format(e))


def ftp_auth(check):
    from ftplib import FTP
    anonymous = True
    with FTP(check.host.ip) as ftp:
        try:
            if 'anonymous' in check.notes.lower():
                ftp.login()
            else:
                username = check.service.credential.username
                password = check.service.credential.password
                ftp.login(username, password)
            return_value = ftp.getwelcome()
            
            return (True, 'FTP Authentication Succeeded - "{}"'.format(return_value))
        except Exception as e:
            return (False, 'FTP Authentication Failed - Error: "{}"'.format(e))
            
plugins = {'FTP': ftp_auth}
            