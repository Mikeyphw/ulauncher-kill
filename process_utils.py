import psutil

def find_by_port(port):
    out=[]
    for c in psutil.net_connections(kind="inet"):
        if c.laddr and c.laddr.port==port and c.pid:
            out.append(c.pid)
    return list(set(out))
