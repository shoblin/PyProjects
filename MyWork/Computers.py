import ipaddress


def check_ip(ip):
    """
    Check is ip address valid or not
    :param ip: string - ip address
    :return: True - Ip address is valid
             False - not valid
    """
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False
    else:
        return True


class Computer:
    """

    :param fqdn (str): Fully Qualified Domain Name
    :param os (str): OS's name
    :param ip (str): ip address. Must be like {1-255}.{0-255}.{0-255}.{0-255}
    :param core (int): VM's number of core
    :param memory (int): VM's RAM
    :param os_disk (int): Value
    :param data_disk (int):

    """
    def __init__(self, fqdn, os, ip,
                 core, memory,
                 os_disk, data_disk):
        self.fqdn = fqdn
        self.name = fqdn.split('.')[0]

        self.os = os

        if check_ip(ip):
            self.ip = ip
        else:
            print('IP address не валидный. Будет заменен на 127.0.0.1')
            input('Press Enter')
            self.ip = '127.0.0.1'

        self.core = core
        self.memory = memory

        self.os_disk = os_disk
        self.data_disk = data_disk

        self.pref = self.tenant()

    def tenant(self):
        pref = self.name[3]
        return pref

    def __str__(self):

        r = f'Name:    {self.name}\n'
        r += '#' * 50 + '\n'
        r += f'FQDN    {self.fqdn}\n'
        r += f'OS:     {self.os}\n'
        r += f'IP:     {self.ip}\n\n'
        r += ' Configure '.center(50, '#') + '\n'
        r += f'CPU Cores:       {self.core} Cores\n'
        r += f'Memory RAM:      {self.memory} Gb\n'
        r += f'OS Disk:         {self.os_disk} Gb\n'
        r += f'Data Disk:       {self.data_disk} Gb'

        return r


#a = Computer('TT1-QUIKAS113.finamtrade.ru', 'Windows Server 2012 STD R2 (64-bit)', '10.0.6.26',
#             16, 36, 40, 200)
#b = Computer()
#print(a)
