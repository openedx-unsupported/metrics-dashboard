#!/usr/bin/env python3
import bcrypt
import sys

passwd = str.encode(sys.argv[1])
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(passwd, salt)
print(hashed.decode())
