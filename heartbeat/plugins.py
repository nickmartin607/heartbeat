def port_connect(ip, port):
    from scapy.all import IP, TCP, sr1
    result = False
    try:
        packet = IP(dst=ip)/TCP(dport=port, flags='S', seq=1000)
        results = sr1(packet, timeout=3)
        if results:
            result = True
            details = '{}:{} Connection Succeeded'.format(ip, port)
        else:
            details = '{}:{} Connection Failed'.format(ip, port)
    except Exception as e:
        details = 'Port Connection Failure - {}:{} Error: "{}"'.format(ip, port, e)
    return {'result': result, 'details': details}

def ping(ip):
    from scapy.all import IP, ICMP, sr1
    result = False
    try:
        packet = IP(dst=ip)/ICMP()
        results = sr1(packet, timeout=3)
        if results:
            result = True
            details = 'Ping Succeeded - {} is Alive'.format(ip)
        else:
            details = 'Ping Succeeded - {} is Down'.format(ip)
    except Exception as e:
        details = 'Ping Failed - {} Error: "{}"'.format(ip, e)
    return {'result': result, 'details': details}

def ftp_auth(*args, **kwargs):
    from ftplib import FTP
    result = False
    try:
        with FTP(kwargs.get('ip')) as ftp:
            try:
                username = kwargs.get('username', 'anonymous')
                if username == 'anonymous':
                    ftp.login()
                else:
                    ftp.login(username, kwargs.get('password', ''))
                result = True
                details = 'FTP {} Auth Success - Results: "{}"'.format(ftp.getwelcome())
            except Exception as e:
                details = 'FTP {} Auth Failed - Error: "{}"'.format(e)
    except Exception as e:
        details = 'General FTP Failure - Error: "{}"'.format(e)
    return {'result': result, 'details': details}
