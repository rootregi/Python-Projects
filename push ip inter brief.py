# importe da biblioteca netmiko
 
from netmiko import ConnectHandler

# definindo os detalhes da conec SSH para os switchs

cisco = {
    'device_type': 'cisco_ios',
    'host': 'ITSSG-LSW30.it.abb.com',
    'username': 'it-rena',
    'password': 'VUlcan@1500',
}

# estabeleca a conec SSH com o switch
net_connect = ConnectHandler(**cisco)

# porta vlan que deseja configurar

interface_name = 'fast0/11'
vlan_id = '300'

config_commands = {
    f'interface {interface_name}',
    f'switchport mode access',
    f'switchport access vlan {vlan_id}',
     'end',

}

# envie os comandos de configuracao para o switch
output = net_connect.send_config_set(config_commands)
#exibir a saida da configuracao
print(output)






