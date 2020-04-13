AUTH_INIT_VAL = 5
TGT_INIT_VAL = 5
AUTH_TICKET_LIFETIME = 24*60*60*60*1000 # 1 Day
TICKET_LIFETIME = 10*60*1000 #10 min

SERVER_INIT_RAND_MIN = 1
SERVER_INIT_RAND_MAX = 2147483647

REQ_INIT_VAL = 5

from .kerberos_KDC.kerberos_as import Kerberos_AS
from .kerberos_KDC.kerberos_tgs import Kerberos_TGS
from .kerberos_KDC import Kerberos_KDC

from .crypto_classes import Cryptor,AES_Cryptor

from .db_classes import DB,Local_db

from .interface_classes import User

from .kerberos_server import Server

from .ServerError import ServerError

from .kerberso_client import client