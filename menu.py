from login import verify_login_server
from messages import *
from hashtags import *
from subscriptions import *

def show_menu_options():
    print "Please choose from the following options:\n" 
    print "See Offline Messages [offline]"
    print "Edit Subscriptions [edit]"
    print "Post a Message [post]"
    print "Logout [logout]"
    print "Hashtag Search [search]\n"

def choose_menu_func(menu_option, s, addr):
    
    if menu_option == "login":
        verify_login_server(s, addr)
        return True
    elif menu_option == "new_messages_total":
        get_number_of_new_messages_server(s, addr)
        return True
    elif menu_option == "post_message":
        post_message_server(s, addr)
        return True
    elif menu_option == "search":
        search_tags_server(s, addr)
        return True
    elif menu_option == "valid_user":
        is_valid_user_server(s, addr)
        return True
    elif menu_option == "add_subscription":
        add_subscription_server(s, addr)
        return True
    elif menu_option == "get_all_subscriptions":
        show_all_subscriptions_server(s, addr)
        return True
    elif menu_option == "update_subscriptions":
        update_subscriptions_server(s, addr)
        return True
    elif menu_option == "send_to_followers":
        forward_to_followers_server(s, addr)
        return True
    elif menu_option == "see_all_messages":
        see_offline_messages_server(s, addr)
        return True
    elif menu_option == "see_selected_messages":
        see_selected_messages_server(s, addr)
        return True

        
    return False

def perform_option(menu_option, user):
    
    if menu_option == "post":
        post_message(user)
    elif menu_option == "search":
        search_tags()
    elif menu_option == "edit":
        display_edit_menu(user)
    elif menu_option == "offline":
        see_offline_messages(user)
    elif menu_option == "logout":
        return 
    else:
        print "Incorrect menu option. Please try again.\n"
