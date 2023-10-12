import paramiko
import time

# Defina uma lista de endereços IP dos switches Cisco
switches = [
    '192.168.1.154',
    '192.168.1.155',
    '192.168.1.156',
    '192.168.1.157',
    '192.168.1.130',
    '192.168.1.129',
    '192.168.1.128',
    '192.168.1.127',
    '192.168.1.126',
    # Adicione mais endereços IP conforme necessário
]

# Defina as informações de autenticação SSH
username = 'cisco'
password = 'cisco'

# Função para configurar uma interface loopback em um switch
def configurar_loopback(switch_ip, username, password, loopback_number, loopback_ip, loopback_mask):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(switch_ip, username=username, password=password)
        print(f"Conectado ao switch {switch_ip}")
    except paramiko.AuthenticationException:
        print(f"Falha na autenticação no switch {switch_ip}")
        return
    except paramiko.SSHException as e:
        print(f"Falha na conexão SSH ao switch {switch_ip}: {str(e)}")
        return
    except Exception as e:
        print(f"Falha ao conectar-se ao switch {switch_ip}: {str(e)}")
        return

    ssh_shell = ssh_client.invoke_shell()
    time.sleep(1)

    commands = [
        f'enable\n',
        f'cisco\n',
        f'conf t\n',
        f'interface Loopback{loopback_number}\n',
        f'desc Loop-DevNet-RAN\n',
        f'ip address {loopback_ip} {loopback_mask}\n',
        f'end\n',
        f'write memory\n'
    ]

    for command in commands:
        ssh_shell.send(command)
        time.sleep(1)

    time.sleep(2)

    ssh_shell.close()
    ssh_client.close()
    print(f"Interface Loopback{loopback_number} configurada com endereço IP {loopback_ip}/{loopback_mask} no switch {switch_ip}")

# Loop através dos switches e configure as interfaces loopback
loopback_number = 0  # Número inicial da interface loopback
loopback_ip_prefix = '10.0.0.'  # Prefixo do endereço IP

for switch_ip in switches:
    loopback_number += 1
    loopback_ip = f'{loopback_ip_prefix}{loopback_number}'
    loopback_mask = '255.255.255.255'
    configurar_loopback(switch_ip, username, password, loopback_number, loopback_ip, loopback_mask)