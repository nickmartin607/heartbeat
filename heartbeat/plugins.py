def port_connect(ip, port):
    from scapy.all import IP, TCP, sr1
    try:
        packet = IP(dst=ip)/TCP(dport=port, flags='S', seq=1000)
        results = sr1(packet, timeout=3)
        if results:
            return (True, '{}:{} Connection Succeeded'.format(ip, port))
        else:
            return (False, '{}:{} Connection Failed'.format(ip, port))
    except Exception as e:
        return (False, 'Port Connection Failure - {}:{} Error: "{}"'.format(ip, port, e))

def ping(ip):
    from scapy.all import IP, ICMP, sr1
    try:
        packet = IP(dst=ip)/ICMP()
        results = sr1(packet, timeout=3)
        if results:
            return (True, 'Ping Succeeded - {} is Alive'.format(ip))
        else:
            return (False, 'Ping Succeeded - {} is Down'.format(ip))
    except Exception as e:
        return (False, 'Ping Failed - {} Error: "{}"'.format(ip, e))

def ftp_auth(*args, **kwargs):
    from ftplib import FTP
    try:
        with FTP(kwargs.get('ip')) as ftp:
            try:
                username = kwargs.get('username', 'anonymous')
                if username == 'anonymous':
                    ftp.login()
                else:
                    ftp.login(username, kwargs.get('password', ''))
                results = ftp.getwelcome()
                return (True, 'FTP {} Auth Success - Results: "{}"'.format(results))
            except Exception as e:
                return (False, 'FTP {} Auth Failed - Error: "{}"'.format(e))
    except Exception as e:
        return (False, 'General FTP Failure - Error: "{}"'.format(e))
