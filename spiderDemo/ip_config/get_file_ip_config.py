def find_ip():
    fo = open("/tmp/ipConfig.txt", "rw+")
    ss = fo.readline()
    fo.close()
    return ss
