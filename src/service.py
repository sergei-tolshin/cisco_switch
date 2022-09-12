from collections import OrderedDict

from cisco_acl import Ace
from netmiko import ConnectHandler
from prettytable import PrettyTable

from config.settings import srv_settings


class CiscoService:
    def __init__(self, settings: dict):
        self.dev_type = 'cisco_ios'
        self.settings = settings
        self.client = ConnectHandler(
            device_type=self.dev_type, **self.settings)
        self.client.enable()

    def close(self):
        self.client.disconnect()

    def get_version(self):
        command = "sh ver"
        output = self.client.send_command(command, use_textfsm=True)
        return output[0]

    def get_startup_config(self):
        """Стартовая конфигурация коммутатора"""
        command = "sh start"
        output = self.client.send_command(command)
        with open('./output/' + srv_settings.start_cfg_file, 'w') as file:
            file.write(output.replace('!\n', ''))

    def get_running_config(self):
        """Текущая конфигурация коммутатора"""
        command = "sh run"
        output = self.client.send_command(command)
        with open('./output/' + srv_settings.run_cfg_file, 'w') as file:
            file.write(output.replace('!\n', ''))

    def get_acl(self):
        """Сведения о списках контроля доступа (ACL) коммутатора"""
        command = "sh access-lists"
        output = self.client.send_command(
            command,
            use_textfsm=True,
            textfsm_template='./templates/acl.textfsm'
        )

        d = OrderedDict()
        for _ in output:
            if len(_['line']) > 1:
                ace = Ace(line=_['line'], platform='ios')
                d.setdefault((_['name']), list()).append(ace)
        output = [{'name': k, 'lines': v} for k, v in d.items()]

        acl_table = PrettyTable()
        acl_table.field_names = ['name',
                                 'sequence',
                                 'action',
                                 'protocol',
                                 'src_addr',
                                 'src_port',
                                 'dst_addr',
                                 'dst_port',
                                 'option'
                                 ]
        for acl in output:
            name = acl.get('name')
            for ace in acl['lines']:
                acl_table.add_row([name,
                                   ace.sequence,
                                   ace.action,
                                   ace.protocol,
                                   ace.srcaddr.prefix,
                                   ace.srcport.sport,
                                   ace.dstaddr.prefix,
                                   ace.dstport.sport,
                                   ace.option
                                   ])

        return acl_table

    def get_interfaces(self):
        """Сведения об интерфейсах коммутатора"""
        command = "sh int"
        output = self.client.send_command(command, use_textfsm=True)
        interface_table = PrettyTable()
        interface_table.field_names = ['interface',
                                       'ip_address',
                                       'bia_address',
                                       'mtu',
                                       'speed',
                                       'protocol_status',
                                       'description']
        for interface in output:
            interface_table.add_row([interface.get('interface'),
                                     interface.get('ip_address'),
                                     interface.get('address'),
                                     interface.get('mtu'),
                                     interface.get('speed'),
                                     interface.get('protocol_status'),
                                     interface.get('description'),
                                     ])
        return interface_table
