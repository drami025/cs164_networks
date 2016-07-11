import socket
import json
import sys
from sock import create_socket
from subscriptions import show_all_subscriptions, is_valid_user
from hashtags import *
from output_format import *

def get_number_of_new_messages(username):

    s, HOST, PORT = create_socket()
    
    s.sendto("new_messages_total", (HOST, PORT))

    d = s.recvfrom(1024)
    addr = d[1]

    s.sendto(username, addr)

    d = s.recvfrom(1024)

    return d[0]



def post_message(username):
    
    message = raw_input("Enter your message [without hashtags]:\n")
    
    while len(message) > 140:
        print "Message over 140 characters.\n"
        message = raw_input("Enter message again:\n")

    if message == "CANCEL":
        return

    hash_tag_string = raw_input("Enter any hash tags you want:\n")
    hash_tag_string = hash_tag_string.strip()

    if hash_tag_string == "CANCEL":
        return

    while '#' not in hash_tag_string and hash_tag_string != '':
        print 'Invalid hashtag format.\n'
        hash_tag_string = raw_input("Please have a '#' in your input or simply hit [ENTER] if you do not want to include hashtags:\n")
        hash_tag_string = hash_tag_string.strip()

        if hash_tag_string == "CANCEL":
            return

    s, HOST, PORT = create_socket()

    s.sendto("post_message", (HOST, PORT))
    d = s.recvfrom(1024)
    addr = d[1]

    s.sendto(username, addr)
    d = s.recvfrom(1024)
    s.sendto(message, addr)
    d = s.recvfrom(1024)
    s.sendto(hash_tag_string, addr)

    forward_to_followers(username, message)



def forward_to_followers(username, message):
    
    s, HOST, PORT = create_socket()
    s.sendto("send_to_followers", (HOST, PORT))
    d = s.recvfrom(1024)
    addr = d[1]

    s.sendto(username, addr)
    d = s.recvfrom(1024)

    s.sendto(message, addr)


def see_offline_messages(username):
    print_border()

    print 'Enter [all] to see all messages, or enter a valid username to see messages from this user.'
    response = raw_input("Enter option: ")

    if response == "all":
        see_all_messages(username)
    elif response == "CANCEL":
        return
    else:
        while not is_valid_user(response):
            response = raw_input("Invalid user name. Enter valid user: ")

        see_selected_messages(username, response)


def see_all_messages(username):
    
    s, HOST, PORT = create_socket()
    s.sendto("see_all_messages", (HOST, PORT))
    d = s.recvfrom(1024)
    addr = d[1]

    s.sendto(username, addr)
    d = s.recvfrom(1024)

    messages = d[0].split('\n')

    if not messages:
        print 'No new messages available. \n\n'
        return

    print '\n\n All offline messages'
    print '----------------------\n'

    for message in messages:
        print message

    print '\n\n'


def see_selected_messages(username, selected_user):
    
    

    s, HOST, PORT = create_socket()
    s.sendto("see_selected_messages", (HOST, PORT))
    d = s.recvfrom(1024)
    addr = d[1]

    s.sendto(username + " " + selected_user, addr)
    d = s.recvfrom(1024)

    messages = d[0].split('\n')

    if not messages:
        print 'No new messages from ' + selected_user
        return

    if messages[0] == "INVALID":
        print 'Currently not subscribed to ' + selected_user
        return

    print '\n\n  All offline messages from ' + selected_user
    print '-------------------------------------'

    for message in messages:
        print message

    print '\n\n'









def post_message_server(s, addr):
    
    s.sendto("post message okay", addr)
    d = s.recvfrom(1024)

    user = d[0]

    s.sendto("received user", addr)
    d = s.recvfrom(1024)

    message = d[0]

    s.sendto("received message", addr)
    d = s.recvfrom(1024)

    hash_tag_string = d[0]
    hash_tags = hash_tag_string.split('#')

    hash_tags = [tags for tags in hash_tags if tags.strip()]

    all_messages = json.load(open('messages.txt'))

    try:
        user_messages = all_messages[user]
        user_messages["my_messages"] = [message] + user_messages["my_messages"]
        all_messages[user] = user_messages
    except KeyError:
        user_messages = { "my_messages" : [message] }
        all_messages[user] = user_messages

    with open('messages.txt', 'w') as outfile:
        json.dump(all_messages, outfile)


    save_hashtag_message(hash_tags, message)


    
def get_number_of_new_messages_server(s, addr):
    
    s.sendto("new messages total okay", addr)

    d = s.recvfrom(1024)

    username = d[0]

    all_messages = json.load(open('messages.txt'))

    try:
        user_messages = all_messages[username]
        new_messages = user_messages["new_messages"]

        count = 0

        for k, v in new_messages.iteritems():
            count += len(v)

        s.sendto(str(count), addr)
    except KeyError:

        try:
            all_messages[username]["new_messages"] = {}
        except KeyError:
            all_messages[username] = {"my_messsages":[], "new_messages":{}}

        with open('messages.txt', 'w') as outfile:
            json.dump(all_messages, outfile)

        s.sendto("0", addr)


def forward_to_followers_server(s, addr):

    s.sendto("send to all followers okay", addr)

    d = s.recvfrom(1024)

    user = d[0]

    s.sendto("received user", addr)
    d = s.recvfrom(1024)

    message = d[0]


    all_users = json.load(open('users.txt'))

    all_followers = []

    try:
        all_followers = all_users[user]["followers"]
    except KeyError:
        return

    if not all_followers:
        return

    all_messages = json.load(open('messages.txt'))

    for follower in all_followers:
        try:
            new_messages = all_messages[follower]["new_messages"]
            new_messages[user] = [message] + new_messages[user]
            all_messages[follower]["new_messages"] = new_messages
        except KeyError:
            all_messages[follower]["new_messages"][user] = [message]

    with open('messages.txt', 'w') as outfile:
        json.dump(all_messages, outfile)


def see_offline_messages_server(s, addr):
    
    s.sendto("see offline messages okay", addr)

    d = s.recvfrom(1024)

    curr_user = d[0]

    all_messages = json.load(open('messages.txt'))

    new_messages = {}

    response = []

    try:
        new_messages = all_messages[curr_user]["new_messages"]

        for user, messages in new_messages.iteritems():
            for message in messages:
                response += [message]

        response = '\n'.join(response)

        s.sendto(response, addr)
    except KeyError:
        s.sendto('', addr)

    new_messages = {}

    all_messages[curr_user]["new_messages"] = new_messages

    with open('messages.txt', 'w') as outfile:
        json.dump(all_messages, outfile)



def see_selected_messages_server(s, addr):

    s.sendto("see selected offline messages okay", addr)

    d = s.recvfrom(1024)

    response = d[0]
    response = response.split()

    curr_user = response[0]
    selected_user = response[1]

    all_messages = json.load(open('messages.txt'))

    ret_message = []

    try:
        selected_user_messages = all_messages[curr_user]["new_messages"][selected_user]

        for message in selected_user_messages:
            ret_message += [message]

        ret_message = '\n'.join(ret_message)
        
        s.sendto(ret_message, addr)

        all_messages[curr_user]["new_messages"].pop(selected_user)

        with open('messages.txt', 'w') as outfile:
            json.dump(all_messages, outfile)

    except KeyError:
        s.sendto("INVALID", addr)
        return
