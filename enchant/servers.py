import redis
import keyring

passw = keyring.get_password("VALVEDB", "VALVEDB")
r = redis.Redis(host='localhost', port=6379, db=0, password=passw)
ser = str(input("Server >"))
try:
    servers: bytes = r.get("servers")
    servers = servers.decode() + ", " + ser
except:
    r.set("servers", ser)
r.set("servers", servers)
