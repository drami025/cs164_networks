import socket

def create_socket():
    HOST = ''
    PORT = 8888

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error, msg:
        print 'Failed to create socket.'
        return None

    return s, HOST, PORT
