# -*- coding: utf-8 -*-
'''
Задание 15.1b

Проверить работу функции get_ip_from_cfg из задания 15.1a на конфигурации config_r2.txt.

Обратите внимание, что на интерфейсе e0/1 назначены два IP-адреса:
interface Ethernet0/1
 ip address 10.255.2.2 255.255.255.0
 ip address 10.254.2.2 255.255.255.0 secondary

А в словаре, который возвращает функция get_ip_from_cfg, интерфейсу Ethernet0/1
соответствует только один из них (второй).

Скопировать функцию get_ip_from_cfg из задания 15.1a и переделать ее таким образом, чтобы она возвращала список кортежей для каждого интерфейса.
Если на интерфейсе назначен только один адрес, в списке будет один кортеж.
Если же на интерфейсе настроены несколько IP-адресов, то в списке будет несколько кортежей.

Проверьте функцию на конфигурации config_r2.txt и убедитесь, что интерфейсу
Ethernet0/1 соответствует список из двух кортежей.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды, а не ввод пользователя.

'''
import re

def get_ip_from_cfg(filename):
    result={}
    with open(filename) as f:
        
        matches = re.finditer(r'interface (\S+)[^!]*?'
                              r' ip address (\S+) (\S+)\s*\S* *\S* *'
                              r'(\d+\.\d+\.\d+\.\d+)* *(\d+\.\d+\.\d+\.\d+)*',f.read())
        for match in matches:
            if match.group(4)==None:
                result[match.group(1)]=match.groups()[1:3]
            else:
                result[match.group(1)]=[match.groups()[1:3],match.groups()[3:5]]

    return result

if __name__=='__main__':
    print(get_ip_from_cfg('config_r2.txt'))
          