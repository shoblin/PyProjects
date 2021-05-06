import Configuration as cnf
import keyring as kr
import requests
import json


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


def hostname_formate(raw_names):
    """
    Raw name we are convert into list with host names
    Args:
        raw_names: servers' names from JIRA's response have format: 'hostname()'

    Returns:
    """
    names = []
    for raw_name in raw_names:
        name = raw_name.split()
        names.append(name[0])
    return names


def get_hosts(session):
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
    hosts = hostname_formate(host_names_raw)

    return hosts
