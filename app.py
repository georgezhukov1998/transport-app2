import sys
app_path = './app_db/'
sys.path.insert(0, app_path)
import inspect
import pkgutil
import time
modules_list = []
#поиск и загрузка всех подключаемых модулей
for module_finder, name, ispkg in pkgutil.iter_modules(path=['./core/']):
    if ispkg or name == __name__: continue
    locals()[name] = module_finder.find_module(name).load_module(name)
    modules_list.append(name)

#Программа вычисления маршрутов между заданными точками:
#Что умеет - считать прямые маршруты и маршруты с 1 пересадкой, определять пройденное расстояние, тип транспорта, время поездки и стоимость презда(прямые маршруты)
#Что будет уметь - время ожидания и время в пути с учетом пересадок
#Разработчик - Жуков Г.К
#Москва, 2018

ct=time.strftime('%X').split(':')
ctm_main = int(ct[0])*60 + int(ct[1])

start_city = input('Место отправления: ')
end_city = input('Место назначения: ')
if start_city==end_city: print('Вы уже в ' + start_city)
in_route = read_lib.route_read(app_path + 'tr_scheme.txt') #чтение - схема всех маршрутов
in_length,rev_in_length = read_lib.graph_read(app_path + 'map.txt') #чтение - длины между городами
in_time = read_lib.timetable_read(app_path + 'timetable.txt') #чтение - расписание всех маршрутов
trip = search_engine.Trip(start_city,end_city,in_route)
translation_table = dict.fromkeys(map(ord, "',[]AZE"), None) #Unicode таблица символов, удаляемых из вывода
if trip.straight_routes!=[] and start_city!=end_city:
    trip_time_all = {}
    trip_tax_all = {}
    waiting_time_all = {}
    print('\nПРЯМЫЕ МАРШРУТЫ: ' +str(trip.straight_routes).translate(translation_table))
    for route in trip.straight_routes:
        d1=trip.cropp(start_city,end_city,route) #обрезанный маршрут (от точки отправления до точки назначения)
        len_straight = financial_addon.calc_length(d1,in_length,rev_in_length) #длина этого маршрута
        d2=trip.cropp(in_route[route][0],start_city,route) #обрезанный маршрут (от депо до точки отправления)
        len_straight_to = financial_addon.calc_length(d2,in_length,rev_in_length) #длина этого маршрута
        transport_type = financial_addon.transport_type(route) #тип транспортного вредства
        trip_time=financial_addon.trip_time(route,len_straight[route]) #время поездки
        trip_time_all[route]=trip_time #записать в словарь для вычисления самого быстрого маршрута (+это может пригодиться в сортировке)
        trip_time_hrs=int(trip_time) #время поездки(часы)
        trip_time_min=int((trip_time-trip_time_hrs)*60) #время поездки(минуты)
        waiting_time=financial_addon.calc_waiting(in_time,route,len_straight_to) #время ожидания в минутах
        waiting_time_all[route]=waiting_time #записать в словарь для вычисления ближайшего маршрута (+это может пригодиться в сортировке)
        fixed_part = 15 #фиксированная ставка
        per_one_kilometer = 3 #дополнительная ставка за каждый километр
        time_cost_per_minute = 4 #стоимость затраченного времени за одну минуту
        trip_tax=fixed_part+per_one_kilometer*len_straight[route] + time_cost_per_minute*(trip_time_hrs*60+trip_time_min) #стоимость билета
        trip_tax_all[route]=trip_tax #записать в словарь для вычисления самого дешевого маршрута (+это может пригодиться в сортировке)
        print(transport_type + ' №' + str(route.translate(translation_table)) + ': от ' + start_city + '...еще ' + str(len(d1[route])-1) + ' до ' + end_city)
        print('Общая протяженность маршрута: ' + str(len_straight[route]) + ' км.')
        print('Длительность поездки составляет ' + str(trip_time_hrs)+' ч. '+ str(trip_time_min) +' мин.')
        print('Cтоимость проезда: ' + str(trip_tax) + ' у.е.')
        print('Следующий '+transport_type.lower()+ ' прибудет через ' + str(waiting_time) + ' мин.\n')
    min_time = financial_addon.get_minimal(trip_time_all)
    min_tax = financial_addon.get_minimal(trip_tax_all)
    min_waiting = financial_addon.get_minimal(waiting_time_all)
    print('САМЫЙ БЫСТРЫЙ - ' + min_time.translate(translation_table))
    print('САМЫЙ ДЕШЕВЫЙ - ' + min_tax.translate(translation_table))
    print('БЛИЖАЙШИЙ - ' + min_waiting.translate(translation_table) + '\n')
elif start_city!=end_city:
    print('Нет прямых маршрутов.')
trip.fractal_list_gen()
trip.filter()
if trip.routes_at_end!=[] and trip.routes_at_start!=[] and trip.list_!=[] and start_city!=end_city:
    print('МАРШРУТЫ С ПЕРЕСАДКАМИ: ' + str(trip.routes_at_start).translate(translation_table))
    trip.path_renewal()
    total_trip_time_all = {}
    total_trip_tax_all = {}
    waiting_for_first = {}
    for rt in trip.total_trip:
        first_route=rt[0][rt[1][0]] #первый маршрут
        second_route=rt[0][rt[1][2]] #второй маршрут
        first_transport=rt[1][0] #первый транспорт(номер маршрута)
        ch_point=rt[1][1] #точка пересадки
        second_transport=rt[1][2] #второй транспорт(номер маршрута
        transport_type_1 = financial_addon.transport_type(first_transport) # первый транспорт(тип транспорта)
        transport_type_2 = financial_addon.transport_type(second_transport)# второй транспорт(тип транспорта)
        print(transport_type_1 +' №'+first_transport.translate(translation_table)+': от ' + start_city + '...еще ' + str(len(first_route)) + ' до ' + str(ch_point) + '-->' + transport_type_2 + ' №' + str(second_transport.translate(translation_table)) + '... ' + str(len(second_route)) + ' до ' + end_city)
        len_first_part=financial_addon.calc_length(rt[0],in_length,rev_in_length)[rt[1][0]] #длина первой части
        len_second_part=financial_addon.calc_length(rt[0],in_length,rev_in_length)[rt[1][2]] #длина второй части
        total_len=len_first_part+len_second_part #вся длина маршрута
        trip_time_1=financial_addon.trip_time(first_transport,len_first_part)*60 #время пушетествия по первому в минутах
        trip_time_2=financial_addon.trip_time(second_transport,len_second_part)*60 #время путешествия по второму в минутах
        c=trip.cropp(in_route[first_transport][0],start_city,first_transport) #обрезанный первый маршрут (от депо до точки отправления)
        len_to_first = financial_addon.calc_length(c,in_length,rev_in_length) #длина от депо до места отправления
        waiting_time_1=financial_addon.calc_waiting(in_time,first_transport,len_to_first) #время ожидания первого в минутах
        waiting_for_first[first_transport]=waiting_time_1
        waiting_time_2=financial_addon.calc_waiting(in_time,second_transport,{second_transport:0},ctm=ctm_main+trip_time_1) #время ожидания второго в минутах (на пункте пересадки)    
        total_trip_time_min=trip_time_1+trip_time_2 + waiting_time_2 #Итоговое время в минутах с учетом пересадки
        total_trip_time_all[transport_type_1+' '+str(first_transport)+' - '+transport_type_2+' '+str(second_transport)]=total_trip_time_min
        trip_time_hrs=total_trip_time_min/60
        trip_time_min=int((trip_time_hrs-int(trip_time_hrs))*60)
        trip_time_hrs=int(trip_time_hrs)
        fixed_part = 15 #фиксированная ставка
        per_one_kilometer = 3 #дополнительная ставка за каждый километр
        time_cost_per_minute = 4 #стоимость затраченного времени за одну минуту
        trip_tax_1=fixed_part+per_one_kilometer*len_first_part #такса за первую часть поездки
        if transport_type_1 == transport_type_1: fixed_part = 5 #изменить фикс.часть, если транспорт одинаковый
        trip_tax_2=fixed_part+per_one_kilometer*len_second_part #такса за вторую часть поездки
        trip_tax = trip_tax_1 + trip_tax_2 + 4*total_trip_time_min #итоговая такса с учетом затрат времени
        total_trip_tax_all[transport_type_1+' '+str(first_transport)+' - '+transport_type_2+' '+str(second_transport)]=trip_tax   
        #записать в словарь для вычисления самого дешевого маршрута (+это может пригодиться в сортировке)
        print(rt[1][2] + ' ' + str(waiting_time_2))
        print('Общая протяженность маршрута: ' + str(total_len) + ' км.')
        print('Длительность поездки составляет ' + str(trip_time_hrs)+' ч. ' + str(trip_time_min)+' мин.')
        print('Следующий '+transport_type_1.lower()+ ' прибудет через ' + str(waiting_time_1) + ' мин.')
        print('Ожидание на пункте пенесадки составит: ' + str(int(waiting_time_2)) + ' мин.\n')
    min_time = financial_addon.get_minimal(total_trip_time_all)
    min_tax = financial_addon.get_minimal(total_trip_tax_all)
    min_waiting = financial_addon.get_minimal(waiting_for_first)
    print('САМЫЙ БЫСТРЫЙ ПУТЬ - ' + min_time.translate(translation_table))
    print('САМЫЙ ДЕШЕВЫЙ ПУТЬ - ' + min_tax.translate(translation_table))
    print('БЛИЖАЙШИЙ ТРАНСПОРТ - ' + min_waiting.translate(translation_table) + '\n')
elif start_city!=end_city:
    print('Нет маршрутов с пересадками.\n')

#ЗАДАЧА - организовать модульный вывод сообщений. Т.е определение пути, длины пути, стоимости поездки, и вычисление ожидания - все разные модули! и вывод будет производиться только если есть модуль, отвечающий за вывод сообщения. а вывод сообщения прописан в самом модуле.


