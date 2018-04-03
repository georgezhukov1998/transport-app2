def main():
    print(__name__)
def route_read(filename):
    """Чтение файла, содержащего все маршруты и запись в словарь"""
    route_list = {}
    with open(filename) as f:
        for line in f:
            line = line.rstrip('\n')
            ltt = line.split('    ')
            route_list[ltt[0]] = ltt[1:]
    return route_list
def graph_read(filename):
    """Чтение файла, содержащего все соединения между городами и запись в словарь"""  
    length_list = {}
    rev_length_list = {}
    with open(filename) as f:
        for line in f:
            line = line.rstrip('\n')
            ltt = line.split('    ')
            if len(ltt) < 3: continue
            if ltt[0] in length_list:length_list[ltt[0]].append([ltt[1],ltt[2]])    
            else:length_list[ltt[0]] = [[ltt[1],ltt[2]]]
            if ltt[1] in rev_length_list:rev_length_list[ltt[1]].append([ltt[0],ltt[2]])
            else:rev_length_list[ltt[1]] = [[ltt[0],ltt[2]]]
    return length_list,rev_length_list

def timetable_read(filename):
    time_list = {}
    with open(filename) as f:
        for line in f:
            line = line.rstrip('\n')
            ltt = line.split('    ')
            if ltt[0] in time_list: time_list[ltt[0]].append(ltt[1:])
            else: time_list[ltt[0]] = ltt[1:]
    return time_list
