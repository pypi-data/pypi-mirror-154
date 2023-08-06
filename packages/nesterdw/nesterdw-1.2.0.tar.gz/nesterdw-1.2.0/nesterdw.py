"""This is the nester.py module which contains a function called print_lol() dedicated at printing lists
including splitting sub-lists down to elements"""

def print_lol(the_list, tab_number=0):
    """print_lol() printing elements of the lists,
    splitting sub-lists down to elements.
    Each sublist is indented by tab_number tab stops"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, tab_number+1)
        else:
            for tab_stop in range(tab_number):
                print("\t", end='')
            print(each_item)
