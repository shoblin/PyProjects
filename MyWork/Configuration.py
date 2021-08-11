"""
##############################
########## KEYRING ###########
##############################
"""
# keyring jira
sys_name_keyring = "jira-sd"
login_keyring = "tscontrol-p"

jira_url = "https://sd.finam.ru"

# Default root linux server
linux_root_name_keyring = "linux_root"

# keyring linux server
linux_sys_name_keyring = "linux"
linux_login_keyring = "topolskiy"

# keyring zabbix server
zabbix_name_keyring = "zabbix"
zabbix_login_keyring = "api-readonly-new"

"""
##############################
###########  API  ############
##############################
"""
# Issue API section
td_api_url = "/rest/api/2/search?jql=issue="
field_hostname = "customfield_21001"

# Object card API section
insight_api_url = "/rest/insight/1.0/iql/objects"

#
dns = {
    "MSA": ["10.77.196.10", "10.77.96.10"],
    "MSK": ["10.77.96.10", "10.77.196.10"],
    "TT1": ["10.77.4.100", "10.77.36.100"],
    "TT2": ["10.77.36.100", "10.77.4.100"],
    "FRN": ["10.200.32.10", "10.200.96.10"],
    "FRE": ["10.200.96.10", "10.200.196.5"],
    "FRX": ["10.200.196.5", "10.200.96.10"],
    "NYA": ["10.200.128.10", "10.200.160.10"],
    "NYX": ["10.200.160.10", "10.200.128.10"]
    }

time_zones = [
    {"prefix": ["TT1", "TT2", "MSA", "MSK"], "tz": "Europe/Moscow"},
    {"prefix": ["FRX", "FRE"], "tz": "Europe/Berlin"},
    {"prefix": ["NYX", "NYA"], "tz": "America/New_york"}
    ]

ATTR_ID = {
    "fqdn": 598,         # Fully Qualified Domain Name
    "os_disk": 1475,     # Size of Disks
    "data_disk": 1477,
    "ip": 227,           # Ip Address
    "core": 1473,
    "memory": 1474,
    "os": 221
    }

# Linux base configuration
config_network = """
source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
allow-hotplug ens192
iface ens192 inet static
        address {0}
        netmask 255.255.255.0
        gateway 10.200.96.1"""

config_hostname = "echo {} > /etc/hostname"
config_timezone = "timedatectl set-timezone {}"

config_resolv = "echo 'domain {0}' > /etc/resolv.conf,echo 'search {0}' >> /etc/resolv.conf," \
                "echo 'nameserver {1}' >> /etc/resolv.conf,echo 'nameserver {2}' >> /etc/resolv.conf"
