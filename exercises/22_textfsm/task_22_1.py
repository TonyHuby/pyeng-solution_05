# -*- coding: utf-8 -*-
'''
Задание 22.1

Создать функцию parse_command_output. Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список:
* первый элемент - это список с названиями столбцов
* остальные элементы это списки, в котором находятся результаты обработки вывода

Проверить работу функции на выводе команды output/sh_ip_int_br.txt и шаблоне templates/sh_ip_int_br.template.

'''
from textfsm import TextFSM
from pprint import pprint
def parse_command_output(template,command_output):
    with open(template) as f:
        tabl=TextFSM(f)
        headers=tabl.header
        res = tabl.ParseText(command_output)
    return [headers,res]


if __name__=='__main__':
    with open('output/sh_ip_int_br.txt') as ff:
        pprint(parse_command_output('templates/sh_ip_int_br.template',ff.read()))
