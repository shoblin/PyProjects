import ipaddress
import paramiko
import keyring
import re
import Configuration as cnf


class Computer(object):
    """
    fqdn (str): Fully Qualified Domain Name
    os (str): OS's name
    ip (str): ip address. Must be like {1-255}.{0-255}.{0-255}.{0-255}
    core (int): VM's number of core
    memory (int): VM's RAM
    os_disk (int): Value
    data_disk (int):
    """

    def __init__(self, name):
        self.name = name
        self.fqdn = self.name + "domain.ru"

        self.ip = "127.0.0.1"
        self.core = 1
        self.memory = 1

        self.os_disk = 10
        self.data_disk = 10

        self.os = "Os"

    def __str__(self):
        r = f'Name:    {self.name} || {self.name.upper()} \n'
        r += '#' * 50 + '\n'
        r += f'FQDN    {self.fqdn}\n'
        r += f'OS:     {self.os}\n'
        r += f'IP:     {self.ip}\n\n'
        r += ' Configure '.center(50, '#') + '\n'
        r += f'CPU Cores:       {self.core} Cores\n'
        r += f'Memory RAM:      {self.memory} Gb\n'
        r += f'OS Disk:         {self.os_disk} Gb\n'
        r += f'Data Disk:       {self.data_disk} Gb\n'

        return r

    def check_ip(self, ip):
        """
            Check is ip address valid or not
            :param ip: string - ip address
            :return: True - Ip address is valid
                     False - not valid
            """
        try:
            ipaddress.ip_address(self.ip)
        except ValueError:
            return False
        else:
            return True

    @property
    def prefix(self):
        return self.name.split("-")[0].upper()

    @property
    def domain(self):
        domain = self.fqdn.replace(self.name + ".", "")
        return domain

    @property
    def t_zone(self):
        """"""
        for time_zone in cnf.time_zones:
            if self.prefix in time_zone['prefix']:
                return time_zone["tz"]
        return "Europe/Moscow"

    def conf_linux_sever(self):
        user = 'root'
        secret = keyring.get_password('linux_root', user)
        port = 22

        with paramiko.SSHClient() as client:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Подключение к серверу
            client.connect(hostname=self.ip, username=user, password=secret, port=port)

            # Меняем содержимое файла hostname на <self.fqdn>
            print(f'Записываем в hostname {self.fqdn}')
            client.exec_command(cnf.config_hostname.format(self.fqdn))
            print('Ok', "", sep="\n")

            # Меняем resolv.conf
            print('Записываем в resolv.conf')
            pref = self.prefix
            resolv_conf = cnf.config_resolv.format(self.domain, cnf.dns[pref][0], cnf.dns[pref][1])

            for command in resolv_conf.split(','):
                client.exec_command(command)
            print('Ok', "", sep="\n")

            # Изменяем Time Zone сервера
            client.exec_command(cnf.config_timezone.format(self.t_zone))

            client.exec_command("shutdown -r 0")


if __name__ == "__main__":
    a = Computer('FRA-TEST-TS1.test.orc')
    print(a.t_zone)