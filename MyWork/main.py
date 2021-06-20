# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import fa


def print_computers(computers):
    """
    Output information about Computers

    Args:
        computers: list with objects - Computer

    """
    for comp in computers:
        print(comp)
        input('Нажмите любую кнопку...')


def main():
    session = fa.create_jira_session()
    hosts = fa.get_host_id(session)

    full_cards = fa.get_cards(session, hosts)
    computers = fa.get_server(full_cards)

    print_computers(computers)

    print('Для начала настройки серверов')
    input('Нажмите кюбую кнопку... ')
    for comp in computers:
        comp.conf_linux_sever()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
