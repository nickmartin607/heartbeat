import dns, ftplib, socket

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
