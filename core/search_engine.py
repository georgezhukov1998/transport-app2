#ВНИМАНИЕ! пока что не распознает кольцевые маршруты 
#(ввести правило - ЕСЛИ - какая либо точка встречается и в конце и в начале, рассматривать линию как кольцевую, 
#и рассчитывать как две прямых линии (налево и направо от точки отправления)
def main():
    print(__name__)
import copy
class Trip():
    def __init__(self,start_city,end_city,in_route):
        self.in_route=in_route
        self.cin_route=copy.copy(in_route)
        self.start_city=start_city
        self.end_city=end_city
        self.exclude = {key:value for key,value in self.in_route.items() if self.start_city not in self.in_route[key]}
        self.include = {key:value for key,value in self.in_route.items() if self.start_city in self.in_route[key]}
        self.routes_at_start = [key for key in self.in_route.keys() if self.start_city in self.in_route[key]] 
        #СПИСОК маршрутов, пересекающих начальную точку
        self.routes_at_end = [key for key in self.in_route.keys() if self.end_city in self.in_route[key]] 
        #СПИСОК маршрутов, пересекающих конечную точку
        self.straight_routes = [key for key in self.routes_at_start if key in self.routes_at_end] 
        #СПИСОК прямых маршрутов между начальной и конечной точкой
        for key in self.straight_routes:
            if key in self.routes_at_start: self.routes_at_start.remove(key)
            if key in self.routes_at_end: self.routes_at_end.remove(key)
            #здесь - исключить прямые маршруты из маршрутов в начальной и конечной точках, чтобы не искать по ним пересадки
        self.list_=list()
        self.i=0
        self.path={}

    def fractal_list_gen(self): 
        """Рекурсивная функция поиска пересадок"""
        icc = []
        include_new={}
        exclude_new={}
        for change_fr in self.include.keys():#из достижимых узлов (reachable)
            for change_to in self.exclude.keys(): #просмотреть недостижимые (unreachable)
                ic=list(set(self.include[change_fr]) & set(self.exclude[change_to])) #и понять где они пересекаются, если пересекаются
                conditional=change_fr not in self.straight_routes and change_to not in self.straight_routes
                if ic!=[] and change_to!=change_fr and conditional:
                    self.list_.append([change_fr,ic,change_to]) #запись в лист пересадок
                    icc = icc+ic
        self.in_route={key:value for key,value in self.in_route.items() if key not in self.include.keys()} 
        #новый in_route, не включающий старый include
        for city in list(set(icc)):
            self.include={key:value for key,value in self.in_route.items() if city in self.in_route[key]}
            self.exclude={key:value for key,value in self.in_route.items() if city not in self.in_route[key]}
            include_new = {**self.include, **include_new}
            self.include = copy.copy(include_new)
            exclude_new = {**self.exclude, **exclude_new}
            self.exclude = copy.copy(exclude_new)
            #новые include и exclude, учитывающие достигнутые города (icc - список достигнутых городов)
        self.i+=1
        self.clist_=copy.copy(self.list_)
        if self.i<=0:
            self.fractal_list_gen() #условная рекурсия

    def cropp(self,start,finish,what_route):   
        """функция обрезки маршрутов от точки А до точки Б по определенному маршруту"""
        p={}
        pss=copy.copy(self.cin_route[what_route])
        if not finish in pss or not start in pss: return 0
        il=pss.index(start)
        ir=pss.index(finish)+1
        if pss[il:ir]==[]: #если срез пуст, значит, возможно, искать нужно в обратном направлении. работоспособно
            css = pss[ir-1:il+1]
            css.reverse()
        else:css=pss[il:ir]
        p[what_route]=css
        return p
    def filter(self): 
        for i in range(0,len(self.clist_)):
            if self.clist_[i][2] not in self.routes_at_end:self.list_.remove(self.clist_[i])
            #пока что всего одно правило для количества пересадок, равного 1
    def path_renewal(self): 
        """Функция восстановления путей по имеющимся узлам. Поддерживает максимум 1 пересадку."""
        self.total_trip=[]
        self.t=self.routes_at_start + self.routes_at_end
        self.tr=copy.copy(self.t)
        #для поддержки количества пересадок более 1 здесь нужно организовать рекурсию
        #также сделать изменения в cropp для поддержки более 1 пересадки
        self.pdi = self.p_rn(self.start_city,'point',self.routes_at_start)
        self.di = self.p_rn('point',self.end_city,self.routes_at_end)
        for i in self.pdi:
            for di in self.di:
                if list(di.values())[0][0] == list(i.values())[0][-1]:
                    self.total_trip.append([{**i,**di},list(i.keys())+[list(i.values())[0][-1]]+list(di.keys())])

    def p_rn(self,start,end,what_route):
        """Процедура восстановления пути от начальной точки до пересадки и от пересадки до конечной точки.
            Поддерживает максимум 1 пересадку."""
        ins=[]
        for route in what_route:
            for i in self.list_:
                for point in i[1]:
                    if end=='point':x=self.cropp(start,point,route)
                    elif start=='point':x=self.cropp(point,end,route)
                    if x!=0 and route in self.tr and x not in ins: ins.append(x)
            self.tr.remove(route) #для отсутствия повторений
        return ins
