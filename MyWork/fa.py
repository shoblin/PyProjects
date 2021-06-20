import Configuration as cnf
import Computers as cmp
import keyring as kr
import requests


def create_jira_session():
    """
    https://code.tutsplus.com/ru/tutorials/using-the-requests-module-in-python--cms-28204
    Create Session for connection to JIRA

    Returns:
        session (object) - connection parameters for create connects to JIRA
    """
    login = cnf.login_keyring
    passwd = kr.get_password(cnf.sys_name_keyring, cnf.login_keyring)

    session = requests.Session()
    session.auth = (login, passwd)

    return session


def hostname_format(raw_names):
    """
    Raw name we are convert into list with host names
    Args:
        raw_names:  servers' names from JIRA's response have format: 'hostname()'
                    FRE-MMAR01-TR02 (IT-41995)

    Returns:
        host_id: list with server's ids
    """
    host_ids = []
    print(raw_names)
    for i in range(1, len(raw_names), 2):
        id = raw_names[i].split()[1]
        id = id.split('-')[1].strip(')')
        host_ids.append(id)
    return host_ids


def get_host_id(session):
    """

    Args:
        session: connection parameters for create connects to JIRA

    Returns:
        hosts (list[str]): list with all servers' hostnames from issue api response
    """

    # Get issue key and request api_url
    td = input('Enter issue TD:')
    api_url = cnf.jira_url + cnf.td_api_url + td
    issue_objects = session.get(api_url).json()
    td_fields = issue_objects['issues'][0]['fields']
    host_names_raw = td_fields[cnf.field_hostname]

    return hostname_format(host_names_raw)


def get_cards(session, ids):
    """
    Get hosts cards from Insight
    Args:
        ids: list with hostnames
        session: connection parameters for create connects to JIRA

    Returns:
        cards: information about server in JSON
    """
    url = cnf.jira_url
    api = cnf.insight_api_url

    iql = 'objectId IN (' + ", ".join(ids) + ')'
    params = [('objectSchemaId', 2), ('iql', iql), ('resultPerPage', 10000)]
    cards = session.get(url=url + api, params=params).json()

    return cards


def get_server(cards):
    """
    Get server's all attributes from card
    Necessary attributes we get from Configuration.ATTR_ID. It is a diction {NAME: objectTypeAttributeId}
    Args:
        cards: JSON with all server's Attributes

    Returns:

    """
    computers = []
    for card in cards['objectEntries']:

        new_computer = cmp.Computer(card["label"])
        for attr, attr_id in cnf.ATTR_ID.items():
            attr_value = get_attribute_value(card, attr_id)
            setattr(new_computer, attr, attr_value)

        computers.append(new_computer)

    return computers


def get_attribute_value(card, attr_id):
    """

    Args:
        card:
        attr_id:
    Returns:
        value:
    """
    for attribute in card['attributes']:
        if attribute.get('objectTypeAttributeId') == attr_id:
            return attribute['objectAttributeValues'][0]['displayValue']
    return None





