from datetime import timedelta

SECRET_KEY = "xy7gof9O0a7a0I3004ro70bwOlc40slkIlict16oO2rk1go2z04tOynf2lp73oOa"
PERMANENT_SESSION_LIFETIME =  timedelta(minutes=15)
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True

LDAP_SCHEMA = "ldap"
LDAP_DOMAIN = "links.int"
LDAP_HOST = "ldap"
LDAP_PORT = 389
LDAP_USE_SSL = False
LDAP_BASE_DN = "ou=Domain Users,dc=links,dc=int"
LDAP_BIND_DIRECT_CREDENTIALS = True
LDAP_USERNAME = "connector"
LDAP_PASSWORD = "Password1"

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "sqlite:////opt/links/db/links.db"
