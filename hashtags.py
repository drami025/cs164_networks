import json
from sock import *


def save_hashtag_message(hash_tags, message):
    
    all_tags = json.load(open('hash_tags.txt'))

    for tags in hash_tags:
        try:
            all_tags[tags] = [message] + all_tags[tags]
        except KeyError:
            all_tags[tags] = [message]

    with open('hash_tags.txt', 'w') as outfile:
        json.dump(all_tags, outfile)



def search_tags():
    
    print "\n--------------Search Hashtags--------------\n"
    hash_tag = raw_input("Enter a hashtag. (Enter [CANCEL] to go back):\n")

    if hash_tag == "CANCEL":
        return

    s, HOST, PORT = create_socket()

    s.sendto("search", (HOST, PORT))
    d = s.recvfrom(1024)
    addr = d[1]

    s.sendto(hash_tag, addr)
    d = s.recvfrom(1024)

    messages = d[0]

    messages = messages.split('\n')

    i = 0

    print "\n-----All messages-----\n"

    for message in messages:
        print message
        i += 1

        if i >= 10:
            break

    print "\n\n"


def search_tags_server(s, addr):
    
    s.sendto("search okay", addr)

    d = s.recvfrom(1024)
    
    hashtag = d[0]

    all_tags = json.load(open('hash_tags.txt'))

    message_string = ""

    try:
        tag_messages = all_tags[hashtag]
        message_string = '\n'.join(tag_messages)
    except KeyError:
        message_string = "[No message currently exists for this hashtag]"

    s.sendto(message_string, addr)
