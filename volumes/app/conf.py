config = {
    "SECRET_KEY" : "xy7gof9O0a7a0I3004ro70bwOlc40slkIlict16oO2rk1go2z04tOynf2lp73oOa",
    "LDAP_OPENLDAP" : True,
    "LDAP_SCHEMA" : "ldap",
    "LDAP_HOST" : "openldap",
    "LDAP_PORT" : "1389",
    "LDAP_USE_SSL" : False,
    "LDAP_BASE_DN" :  'ou=users,dc=links,dc=int',
    "LDAP_USERNAME" : 'cn=admin,dc=links,dc=int',
    "LDAP_PASSWORD" : 'adminpassword',
    "LDAP_USER_OBJECT_FILTER" : "(&(objectclass=inetOrgPerson)(uid=%s))"
}