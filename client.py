from login import login
from menu import *
from messages import get_number_of_new_messages

while(1):
    is_valid_user, user = login()
    
    if is_valid_user:
        menu_option = ""

        new_messages_count = get_number_of_new_messages(user)

        print "\nWelcome " + user + ".\n"
        print "You have " + new_messages_count + " unread messages.\n"

        while(menu_option != "logout"):
            show_menu_options()
            menu_option = raw_input("\nMenu option: ")
            perform_option(menu_option, user)    
            live_message_count = get_number_of_new_messages(user)

            if menu_option != "logout" and new_messages_count != live_message_count and live_message_count != "0":
                if int(live_message_count) > int(new_messages_count):
                    live_message_count = str(int(live_message_count) - int(new_messages_count))

                print "\n\n-------------------------------------------"
                print 'ALERT: ' + str(live_message_count) + ' new message currently available! Check out your messages [option: offline]'
                print "-------------------------------------------\n"
                total_messages = int(new_messages_count) + int (live_message_count)
                new_messages_count = live_message_count
                print "You have " + str(total_messages) + " unread messages.\n"

        print "\nGoodbye!\n\n"
    else:
        print("Incorrect username/password. Try again.")
