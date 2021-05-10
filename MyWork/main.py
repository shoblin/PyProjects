# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# import Computers as Cmp
import fa
# import json
# import re


def main():
    session = fa.create_jira_session()
    hosts = fa.get_host_id(session)

    full_cards = fa.get_cards(session, hosts)
    computers = fa.get_server(full_cards)

    for comp in computers:
        print(comp)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
