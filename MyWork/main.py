# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import Computers as Cmp
import fa
import json
import re


def main():
    session = fa.create_jira_session()
    hosts = fa.get_hosts(session)
    print(hosts)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
