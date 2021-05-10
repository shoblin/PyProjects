sys_name_keyring = "jira-sd"
login_keyring = "tscontrol-p"

jira_url = 'https://sd.finam.ru'

# Issue API section
td_api_url = '/rest/api/2/search?jql=issue='
field_hostname = 'customfield_21001'

# Object card API section
insight_api_url = '/rest/insight/1.0/iql/objects'

dns = {
    'MSA': ['10.77.196.10', '10.77.96.10'],
    'MSK': ['10.77.96.10', '10.77.196.10'],
    'TT1': ['10.77.4.100', '10.77.36.100'],
    'TT2': ['10.77.36.100', '10.77.4.100'],
    'FRN': ['10.200.32.10', '10.200.96.10'],
    'FRE': ['10.200.96.10', '10.200.196.5'],
    'FRX': ['10.200.196.5', '10.200.96.10'],
    'NYA': ['10.200.128.10', '10.200.160.10'],
    'NYX': ['10.200.160.10', '10.200.128.10']
}

ATTR_ID = { 'fqdn': 598,        # Fully Qualified Domain Name
            'os_disk': 1475,    # Size of Disks
            'data_disk': 1477,
            'ip': 227,          # Ip Address
            'core': 1473,
            'memory': 1474,
            'os': 221
    }