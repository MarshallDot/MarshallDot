import redis

r = redis.Redis(host='localhost', port=5005)
ser = str(input("Server >"))
try:
    servers: bytes = r.get("servers")
    servers = servers.decode() + ", " + ser
except:
    r.set("servers", ser)
r.set("servers", servers)
