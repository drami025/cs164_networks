import socket
import select
import sys
import threading
from menu import choose_menu_func
from sock import create_socket

total_messages_received = 0

class adminThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        global total_messages_received

        while True:
            admin_option = raw_input("")

            if admin_option == "messagecount":
                print 'Total messages received: ' + str(total_messages_received)
        

s, HOST, PORT = create_socket()

try:
    s.bind((HOST, PORT))
    print 'socket binded'
except socket.error, msg:
    print 'Bind error.'
    sys.exit()

inputs = [s]
outputs = []
timeout = 5

thr = adminThread(1, 'admin', 0)
thr.start()

while(1):
    readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)

    for soc in readable:
        d = soc.recvfrom(1024)
        menu_option = d[0]
        addr = d[1]
        
        print addr

        if menu_option == "post_message":
            total_messages_received += 1

        d = choose_menu_func(menu_option, s, addr)

        if d is False:
            print 'Incorrect menu option. Try again' 
