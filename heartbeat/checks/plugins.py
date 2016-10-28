import dns, ftplib, socket, subprocess

def ping(host, ping_count=1, ping_wait=1):
    cmd = ['ping', '-c', str(ping_count), '-w', str(ping_wait), host.ip]
    try:
        return_value = subprocess.check_call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if return_value == 0:
            return (True, 'Ping Succeeded - Host is Alive')
        else:
            return (False, 'Ping Succeeded - Host is Down')
    except Exception as e:
        return (False, 'Ping Failed - Error: "{}"'.format(e))

def port_connect(service=None, ip=None, port=None, timeout=5):
    try:
        ip = service.host.ip if service else ip
        port = port or service.port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        return_value = sock.connect_ex((ip, int(port)))
        if return_value == 0:
            return (True, 'Port {} Connection Succeeded'.format(port))
        else:
            return (False, 'Port {} Connection Failed'.format(port))
    except Exception as e:
        return (False, 'Port Connection Failure - Error: "{}"'.format(e))


def ftp_auth(check):
    anonymous = True
    with ftplib.FTP(check.host.ip) as ftp:
        try:
            if anonymous:
                ftp.login()
            else:
                username = check.service.credential.username
                password = check.service.credential.password
                ftp.login(username, password)
            return_value = ftp.getwelcome()
            return (True, 'FTP Authentication Succeeded - "{}"'.format(return_value))
        except Exception as e:
            return (False, 'FTP Authentication Succeeded - Error: "{}"'.format(e))
            
plugins = {'FTP': ftp_auth}
            


# DNS
#http://www.dnspython.org/examples.html
# https://github.com/bplower/cssef/blob/refactor/plugins/cssefcdc/cssefcdc/plugins/DNS.py
# https://github.com/ubnetdef/scoreengine/blob/master/scoring/checks/dns.py

# LDAP
# http://www.grotan.com/ldap/python-ldap-samples.html
# https://github.com/ubnetdef/scoreengine/blob/master/scoring/checks/ldap.py

# MySQL
# https://github.com/ubnetdef/scoreengine/blob/master/scoring/checks/mysql.py

# HTTP
# https://github.com/bplower/cssef/blob/refactor/plugins/cssefcdc/cssefcdc/plugins/HTTP.py
# https://github.com/ubnetdef/scoreengine/blob/master/scoring/checks/http.py

# SSH
# https://github.com/bplower/cssef/blob/refactor/plugins/cssefcdc/cssefcdc/plugins/SSH.py

# Open Port
# https://github.com/bplower/cssef/blob/refactor/plugins/cssefcdc/cssefcdc/plugins/OpenPort.py
