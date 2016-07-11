import json
from sock import *


def display_edit_menu(curr_user):
    print "\nEnter [add] to add a subscription, [delete] to delete one, or [CANCEL] to return.\n"

    option = raw_input("Option: ")
    
    while True:

        if option == "CANCEL":
            return

        if option == "add":
            user = raw_input("Enter a valid user to subscribe to: ")

            while not is_valid_user(user) and user != "CANCEL":
                user = raw_input("Invalid user. Try again ([CANCEL to quit]): ")

            if user == "CANCEL":
                return

            add_subscription(curr_user, user)
            print "Currently subscribed to " + user + "\n"
            break

        if option == "delete":
            all_subscriptions = show_all_subscriptions(curr_user)

            if not all_subscriptions:
                print "\nYou currently have no subscriptions.\n"
                break

            print "Subcriptions:\n"

            for sub in all_subscriptions:
                print sub
            
            user = raw_input("\nSelect a valid subscription to delete: ")
            
            while user not in all_subscriptions and user != "CANCEL":
               user = raw_input("Invalid user. Try again: ")
            
            if user == "CANCEL":
                return

            all_subscriptions.remove(user)
            update_subscriptions(curr_user, user, all_subscriptions)

            print 'Subscription deleted\n'
            break

        option = raw_input("\nInvalid option. Try again: ")



def is_valid_user(user):
    
    s, HOST, PORT = create_socket()

    s.sendto("valid_user", (HOST, PORT))
    d = s.recvfrom(1024)
    addr = d[1]

    s.sendto(user, addr)
    d = s.recvfrom(1024)

    if d[0] == "True":
        return True

    return False


def add_subscription(curr_user, user):
    
    s, HOST, PORT = create_socket()

    s.sendto("add_subscription", (HOST, PORT))
    d = s.recvfrom(1024)
    addr = d[1]

    s.sendto(curr_user + " " + user, addr)
    


def show_all_subscriptions(curr_user):
    
    s, HOST, PORT = create_socket()

    s.sendto("get_all_subscriptions", (HOST, PORT))
    d = s.recvfrom(1024)
    addr = d[1]

    s.sendto(curr_user, addr)
    d = s.recvfrom(1024)

    all_subscriptions = d[0]

    if not all_subscriptions:
        all_subscriptions = []
    else:
        all_subscriptions = d[0].split('\n')
    

    return all_subscriptions


def update_subscriptions(curr_user, deleted_user, all_subscriptions):
    
    s, HOST, PORT = create_socket()

    s.sendto("update_subscriptions", (HOST, PORT))
    d = s.recvfrom(1024)
    addr = d[1]

    subscript_str = '\n'.join(all_subscriptions)

    s.sendto(curr_user + " " + deleted_user + " " + subscript_str, addr)






def is_valid_user_server(s, addr):

    s.sendto("valid user okay", addr)
    d = s.recvfrom(1024)

    user = d[0]

    all_users = json.load(open("users.txt"))

    try:
        if all_users[user]:
            s.sendto("True", addr)
            return
    except KeyError:
        s.sendto("False", addr)
        

def add_subscription_server(s, addr):
    
    s.sendto("add subscription okay", addr)
    d = s.recvfrom(1024)

    ret_users = d[0]

    ret_users = ret_users.split()

    curr_user = ret_users[0]
    user = ret_users[1]

    all_users = json.load(open("users.txt"))

    try:
        subscriptions = all_users[curr_user]["subscriptions"]

        if user in subscriptions:
            return

        subscriptions = subscriptions + [user]
        all_users[curr_user]["subscriptions"] = subscriptions
    except KeyError:
        all_users[curr_user]["subscriptions"] = [user]


    try:
        followers = all_users[user]["followers"]
        followers = followers + [curr_user]
        all_users[user]["followers"] = followers
    except KeyError:
        all_users[user]["followers"] = [curr_user]


    with open('users.txt', 'w') as outfile:
        json.dump(all_users, outfile)


def show_all_subscriptions_server(s, addr):
    
    s.sendto("all subscriptions okay", addr)
    d = s.recvfrom(1024)

    user = d[0]

    all_users = json.load(open("users.txt"))

    try:
        all_subscriptions = all_users[user]["subscriptions"]
        all_sub_str = '\n'.join(all_subscriptions)
        s.sendto(all_sub_str, addr)
    except KeyError:
        s.sendto('', addr)


def update_subscriptions_server(s, addr):
    
    s.sendto("update subscriptions okay", addr)
    d = s.recvfrom(1024)

    ret_str = d[0]
    ret_str = ret_str.split(' ')

    curr_user = ret_str[0]
    deleted_user = ret_str[1]
    subscriptions = ret_str[2]

    if not subscriptions:
        subscriptions = []
    else:
        subscriptions = subscriptions.split('\n')
        subscriptions = [sub for sub in subscriptions if sub.strip()]

    all_users = json.load(open("users.txt"))

    try:
        all_users[curr_user]["subscriptions"] = subscriptions
    except KeyError:
        all_users[curr_user]["subscriptions"] = []

    
    try:
        followers = all_users[deleted_user]["followers"]
        followers.remove(curr_user)
        all_users[deleted_user]["followers"] = followers
    except KeyError:
        all_users[deleted_user]["followers"] = []


    with open('users.txt', 'w') as outfile:
        json.dump(all_users, outfile)
        
