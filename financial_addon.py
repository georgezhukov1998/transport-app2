def main():
    print(__name__)
import time
import copy
from math import fabs
def calc_length(all_routes,in_length,rev_in_length):
    """Функция вычисления длины маршрута от точки А до точки Б."""
    inline = 0
    tax_out = {}
    for route in all_routes.keys():
        call_routes = copy.deepcopy(all_routes)
        call_routes_2 = copy.deepcopy(all_routes)
        inline = 0
        for point in all_routes[route][:-1]:
            mem = call_routes_2[route].pop(1)
            for x in in_length[point]: 
                if x[0] == mem: inline+=int(x[1])
        if inline == 0: tax_out[route]=calc_rev_length(call_routes[route],rev_in_length)
        #если сумма длин равна нулю, то возможно, следует просмотреть в обратном направлении
        else: tax_out[route]=inline
    return tax_out

def calc_rev_length(route,rev_in_length):
    """Функция вычисления маршрута от точки Б до точки А. Вызывается только из calc_length"""
    inline = 0
    for point in route[:-1]:
        mem = route.pop(1)
        for x in rev_in_length[point]: 
            if x[0] == mem: inline+=int(x[1])
    if inline == 0: return 0 #если же и тут сумма длин между пунктами равна 0, то вернуть 0 окончательно
    else: return inline

def transport_type(route):
    """Возвращает тип транспорта"""
    l_route = list(route)
    t_type = l_route.pop(0)
    if t_type=='A': return 'Автобус'
    elif t_type=='Z': return 'Поезд'
    elif t_type=='E': return 'Электропоезд'
    #перенести типы транспорта и их коды в отдельный лист в файле
    else: return ''

def calc_waiting(in_time,key,length,ctm = int(time.strftime('%X').split(':')[0])*60 + int(time.strftime('%X').split(':')[1])):
    """функция вычисления ожидания того момента, когда автобус прибудет на точку отправления"""
     #текущее время в минутах
    waiting_time = '0'
    start_time = int(in_time[key][3].split(':')[0])*60 + int(in_time[key][3].split(':')[1]) #время начала движения в минутах
    finish_time = int(in_time[key][4].split(':')[0])*60 + int(in_time[key][4].split(':')[1]) #время окончания движения в минутах
    frequency = int(in_time[key][2]) #частота движения (количество пар) в рабочее время
    operating_time = int(finish_time - start_time) #рабочее время в минутах
    interval = int(operating_time/frequency) #интервал движения
    if ctm > (start_time+int(length[key])/40*60): 
        waiting_time = interval - (ctm - start_time)%interval
    else: 
        waiting_time = fabs(int(length[key]/40*60 - (ctm - start_time)))
    return waiting_time

def trip_time(route,len_):
    """Возвращает время движения в зависимости от типа транспорта"""
    l_route = list(route)
    t_type = l_route.pop(0)
    if t_type=='A': return len_/40
    elif t_type=='Z': return len_/60
    elif t_type=='E': return len_/60  
    #перенести типы транспорта и их скорости в лист с кодами (см. комментарий в transport_type)

def get_minimal(dictionary):
    rev_dict = {value:key for key,value in dictionary.items()}
    tt = transport_type(rev_dict[min(dictionary.values())])
    return tt.title() + ' ' + str(rev_dict[min(dictionary.values())])
        
