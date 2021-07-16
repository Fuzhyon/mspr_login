import ssl

from ldap3 import Server, Connection, ALL, SUBTREE, Tls, NTLM
from ldap3.core.exceptions import LDAPException, LDAPBindError

# ldap server hostname and port
ldsp_server = f"ldap://localhost:389"

# dn
root_dn = "dc=example,dc=org"

# ldap user and password
ldap_user_name = 'admin'
ldap_password = 'admin'

# user
user = f'cn={ldap_user_name},root_dn'



server = Server(ldsp_server, get_info=ALL)

connection = Connection(server,
                        user=user,
                        password=ldap_password,
                        auto_bind=True)

print(f" *** Response from the ldap bind is \n{connection}" )


def global_ldap_authentication(user_name, user_pwd):
    """
      Function: global_ldap_authentication
       Purpose: Make a connection to encrypted LDAP server.
       :params: ** Mandatory Positional Parameters
                1. user_name - LDAP user Name
                2. user_pwd - LDAP User Password
       :return: None
    """

    ldap_user_name = user_name.strip()
    ldap_user_pwd = user_pwd.strip()
    tls_configuration = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)
    server = Server('ldap://localhost:389', use_ssl=True, tls=tls_configuration)
    conn = Connection(server, user=ldap_user_name, password=ldap_user_pwd, authentication=NTLM,
                      auto_referrals=False)
    if not conn.bind():
        print(f" *** Cannot bind to ldap server: {conn.last_error} ")
    else:
        print(f" *** Successful bind to ldap server")
    return