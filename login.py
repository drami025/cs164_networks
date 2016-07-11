import getpass
import socket
import json
import sys
from sock import create_socket


def verify_login_client(username, password):

    s, HOST, PORT = create_socket() 

    s.sendto("login", (HOST, PORT))
    
    d = s.recvfrom(1024)

    addr = d[1]

    s.sendto(username + " " + password, addr)

    d = s.recvfrom(1024)

    if d[0] == "True":
        return True

    return False




def verify_login_server(s, addr):
    
    s.sendto("login okay", addr)

    d = s.recvfrom(1024)
    
    login_creds = d[0]

    creds = login_creds.split()

    if len(creds) != 2:
        s.sendto("False", addr)
        return

    all_users = json.load(open('users.txt'))

    username = creds[0]
    password = creds[1]


    try:
        if all_users[username]["password"] == password:
            s.sendto("True", addr)
            return
    except KeyError:
        None

    s.sendto("False", addr)
    



def login():
    username = raw_input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    return verify_login_client(username, password), username
