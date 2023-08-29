import sys
import ldap
import ldap.modlist as modlist
from pprint import pprint


################################################################################
def ldap_search(conn, search='*'):
    base = "dc=ad,dc=vivans,dc=net"
    # base = "dc=example,dc=com"
    criteria = "(name=%s)" % search
    # criteria = "(&(objectClass=user)(sAMAccountName=%s))" % search
    # criteria = "(&(objectClass=user)(sAMAccountName=test))"
    # attributes = ['displayName', 'company']
    attributes = ['*']
    result = conn.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)

    # results = [entry for dn, entry in result if isinstance(entry, dict)]
    results = list()
    for dn, entry in result:
        if not (dn and isinstance(entry, dict)):
            continue
        results.append(entry)
    print('%s' % ('*'*100))
    pprint(results)


################################################################################
def ldap_new_user(l, user_name, user_pass, desc=''):
    # The dn of our new entry/object
    # dn = "cn=%s,dc=ad,dc=vivans,dc=net"
    try:
        dn = 'CN=%s,CN=Users,DC=ad,DC=vivans,DC=net' % user_name

        # A dict to help build the "body" of the object
        attrs = dict()
        attrs['objectclass'] = [b'top', b'person', b'organizationalPerson', b'user']
        attrs['cn'] = user_name.encode()
        attrs['userPassword'] = user_pass.encode()
        attrs['sAMAccountName'] = user_name.encode()
        attrs['description'] = desc.encode()

        # Convert our dict to nice syntax for the add-function using modlist-module
        ldif = modlist.addModlist(attrs)

        # Do the actual synchronous add-operation to the ldapserver
        r = l.add_s(dn, ldif)
        return r
    except Exception as e:
        sys.stderr.write('%s\n' % str(e))
    finally:
        pass


################################################################################
def ldap_modify_dn(l, modify_dn, old, new):
    # Convert place-holders for modify-operation using modlist-module
    ldif = modlist.modifyModlist(old, new)
    # Do the actual modification
    l.modify_s(modify_dn, ldif)


################################################################################
def ldap_delet_dn(l, delete_dn):
    try:
        # you can safely ignore the results returned as an exception
        # will be raised if the delete doesn't work.
        l.delete_s(delete_dn)
    except ldap.LDAPError as e:
        sys.stderr.write('%s\n' % str(e))
    ## handle error however you like


################################################################################
def authenticate(address, username, password, authenticate_only=False):
    conn = ldap.initialize('ldap://' + address)
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    # return
    try:
        r = conn.simple_bind_s(username, password)
        if authenticate_only:
            ldap_search(conn, username)
            return r

        # search
        # ldap_search(conn)
        ldap_new_user(conn, 'myuser123', 'myuser!@#', 'myuser123 added by python-ldap')
        ldap_search(conn, 'myuser*')
        dn = 'CN=%s,CN=Users,DC=ad,DC=vivans,DC=net' % 'myuser123'

        old = {'description': [b'myuser123 added by python-ldap']}
        new = {'description': [b'modified myuser123 added by python-ldap']}
        ldap_modify_dn(conn, dn, old, new)
        ldap_search(conn, 'myuser*')

        # ldap_delet_dn(conn, dn)
        # ldap_search(conn, 'myuser*')

        return r
    except ldap.INVALID_CREDENTIALS:
        sys.stderr.write("Your username or password is incorrect.\n")
    except ldap.SERVER_DOWN:
        sys.stderr.write("The server appears to be down.\n")
    except Exception as e:
        sys.stderr.write('%s\n' % str(e))
    finally:
        conn.unbind()


################################################################################
def test():
    r = authenticate(
        # '192.168.10.61',
        '10.211.55.2',
        'administrator@ad.vivans.net',
        'argos0520!'
    )
    print("authenticate %s" % str(r))

    # r = authenticate(
    #     # '192.168.10.61',
    #     '10.211.55.2',
    #     'myuser123@ad.vivans.net',
    #     'myuser!@#',
    #     authenticate_only=True
    # )
    # print("authenticate %s" % str(r))


################################################################################
if __name__ == '__main__':
    test()
