# -*- coding: utf-8 -*-
'''
Задание 19.2b

Скопировать функцию send_config_commands из задания 19.2a и добавить проверку на ошибки.

При выполнении каждой команды, скрипт должен проверять результат на такие ошибки:
 * Invalid input detected, Incomplete command, Ambiguous command

Если при выполнении какой-то из команд возникла ошибка,
функция должна выводить сообщение на стандартный поток вывода с информацией
о том, какая ошибка возникла, при выполнении какой команды и на каком устройстве, например:
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1

Ошибки должны выводиться всегда, независимо от значения параметра verbose.
При этом, verbose по-прежнему должен контролировать будет ли выводиться сообщение:
Подключаюсь к 192.168.100.1...


Функция send_config_commands теперь должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате:
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.


Пример работы функции send_config_commands:

In [16]: commands
Out[16]:
['logging 0255.255.1',
 'logging',
 'i',
 'logging buffered 20010',
 'ip http server']

In [17]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Команда "i" выполнилась с ошибкой "Ambiguous command:  "i"" на устройстве 192.168.100.1

In [18]: pprint(result, width=120)
({'ip http server': 'config term\n'
                    'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                    'R1(config)#ip http server\n'
                    'R1(config)#',
  'logging buffered 20010': 'config term\n'
                            'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                            'R1(config)#logging buffered 20010\n'
                            'R1(config)#'},
 {'i': 'config term\n'
       'Enter configuration commands, one per line.  End with CNTL/Z.\n'
       'R1(config)#i\n'
       '% Ambiguous command:  "i"\n'
       'R1(config)#',
  'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

In [19]: good, bad = result

In [20]: good.keys()
Out[20]: dict_keys(['logging buffered 20010', 'ip http server'])

In [21]: bad.keys()
Out[21]: dict_keys(['logging 0255.255.1', 'logging', 'i'])


Примеры команд с ошибками:
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#i
% Ambiguous command:  "i"
'''

# списки команд с ошибками и без:
commands_with_errors = ['logging 0255.255.1', 'logging', 'i']
correct_commands = ['logging buffered 20010', 'ip http server']

commands = commands_with_errors + correct_commands

import netmiko
import yaml

def send_show_command(device,commands,verbose=True):
    if verbose:
        print(f'Connect to {device["ip"]}...')
    bad,good = {},{}
    with netmiko.ConnectHandler(**device) as ssh:
        ssh.enable()
        for command in commands:
            res = ssh.send_config_set(command)
            if 'Invalid input detected' in res:
                bad[command]=res
                print(command,f'''falied with error "Invalid input detected" on device {device['ip']}''')
            elif 'Incomplete command' in res:
                bad[command]=res
                print(command,f'''falied with error "Incomlete command" on device {device['ip']}''')
            elif 'Ambiguous command' in res:
                bad[command]=res
                print(command,f'''falied with error "Ambigous command" on device {device['ip']}''')
            else:
                good[command]=res
        
    return (bad, good)

with open('devices.yaml') as f:
    devices = yaml.safe_load(f)
    for device in devices:
        print(send_show_command(device,commands))
        print('-'*20)



