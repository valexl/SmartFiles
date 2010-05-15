'''
Created on 10.04.2010

@author: valexl
'''

class ProcessingRequest(object):
    
    def __init__(self): # конструктор класса
        '''
            конструктор класса
        '''
        self._operators = ['or','and','not','()'] # операции языка запроса
        
        self._table_objs = 'object'
        self._table_objs_tags = 'objects_tags'
        self._table_objs_fields = 'objects_fields'
        self._table_fields = 'fields'   
        self._SQLtables = [self._table_objs, self._table_objs_tags, self._table_objs_fields, self._table_fields] # имена таблиц которые учавствуют в запросе Базе Данных
        
        self._index_using_tables = [0]
        self._field_words = ['>', '>=', '<>', '=', ':', '<=', '<'] 
        
        #>, >=, <>, =, :, <=, <     - знаки которые указывают поиск по полям
        #path="путь к директории"   - path указывает поиск по директории
        #                            Необходимо отделять ключевое слово path от обычного поля path
        #
    
        #self.request = '' 
        #self.cleare_extra_space(user_request); # строка запроса заданная пользователем 
                                                              # переведена в один регистр и без двойных пробелов  
        
        
        
   
            
    def __cleare_extra_space (self,string):    
        '''
        инициализация строки запроса - убираются все лишние пробелы.
        '''
        
        str_lenght = len(string)
        string = string.replace('  ',' ')
        while (str_lenght != len(string)):
            str_lenght = len(string)
            string = string.replace('  ',' ')
        return string.lower().strip() # убираются пробелы с начало и конца строки
        
   
        
        
    def __starting_split (self, request): 
        '''
        
        поиск в запросе операции с наименьшим проритетом и относительно
        этой операции запускается функция разбиение
        
        '''
        operator = 0
        while operator < 3:
            if request.count(self._operators[operator])>0:
                flag = 1
                return self.__split_by_operator(request,operator)
            operator += 1
        return request
    
       
    def __split_by_operator (self,request,operator_index):
        '''
          для заданной строки отделяются операнды от операций OR/ AND / NOT
                                                    
        '''
        list_result = self.__get_spliting_list(request,operator_index)
        operator_index +=1
        while operator_index <3:
            index = 0
            while index<len(list_result):
                if list_result[index].count(self._operators[operator_index]) > 0:
                    list_result[index] = self.__split_by_operator(list_result[index], operator_index)
                    
                index+=1
            
            operator_index +=1
        print(list_result)
        return list_result

    def __get_spliting_list (self,request, operator_index):
        '''
        
        преобразование строки в список из операций и операндов
        
        '''
        list_result= [self._operators[operator_index]]
        if (operator_index == 0) or (operator_index == 1): # для операций AND OR
            list_result+=request.split(self._operators[operator_index])
        #так как операция NOT унарная то она будет отличаться от преобразований AND, OR
        elif (operator_index ==2): # для операции NOT  
            list_result.append(request.split(self._operators[operator_index])[1])
        return list_result    
        
   
    #для представления запроса в древовидной форме используется стандартная функция split. 
    #она представляет строку в виде списка. Остается добавить в этот список только операцию по которой 
    #произошло деление  # Данная функция отлично подходит для операция (and,or,not). Но существет одна
    # проблема. Эта проблема связана с тем, что данная функция не учитывает СКОБКИ (деление происходит так же
    # и в нутри скобок, а это как раз и не допустимо.
    # Для того что бы была возможность учитывать скобки возможны 2а варианта:
    #            1) отделение того что в скобках и вычисление этого отдельно. результат преобразования
    #                запроса в нутри скобок после присоеденияется к искомому результату.
    #            2) сделать аналог split, который не учитывает при деление то, что находится в скобках
    #
    #
    #
    #            Hеализован 1й способ решения.

   
    def __is_list (self, string_list):
        '''
        проверка элемента является ли он списком или нет
        '''
        for operator in self._operators:
            if string_list[0] == operator:
                return 1
        return 0
        
    def __union_request (self,list_request,request_into_brackets):
        '''
         объединение результатов в скобках с искомым
        '''
        index = 0
        for node in list_request:
            if self.__is_list(node):
                self.__union_request(node,request_into_brackets)
            elif node.strip() == self._operators[3]: #скобки
                list_request[index] = ['()',request_into_brackets.pop(0)]
                #print('union request-----',list_request[index])
            index += 1
                
        
        
         
    def __split_request (self,request):       
        '''
         представление строкового запроса в виде вспомогательного списка
        '''       
        count_brackets = request.count('(')
        
        index_open_bracket = request.find('(')
        index_closed_bracket = request.find(')',index_open_bracket)
        modifire_query_string = request[:index_open_bracket] # копирование всего запроса до скобок.
        
                                                            #PS модифицированная строка запроса в процессе выполнение процедурры 
                                                            #получается на основе request путем 
                                                            # вырезания содержимого скобок. Т.е. вместо "(запрос)" 
                                                            #остаются только "()"
                                                            
                                                                        
        list_strings_into_brackets = []  
        #======================================
        #отделение в запросе выражений в скобках
        if count_brackets > 0:
            modifire_query_string+='('
                          
            index = index_open_bracket
            count_brackets-=1
            while count_brackets > 0 :
                count_brackets -=1
                index = request.find('(',index+1)
                if index > index_closed_bracket:
                    modifire_query_string+= request[index_closed_bracket:index+1]
                    list_strings_into_brackets.append(request[index_open_bracket+1:index_closed_bracket])
                    index_open_bracket = index
                    index_closed_bracket = request.find(')',index_open_bracket)
                else:
                    index_closed_bracket = request.find(')',index_closed_bracket+1)
            list_strings_into_brackets.append(request[index_open_bracket+1:index_closed_bracket])
            for pos in range(len(list_strings_into_brackets)):
                list_strings_into_brackets[pos] = self.__split_request(list_strings_into_brackets[pos])
                #print(list_strings_into_brackets[pos])  
        #отделение в запросе выражений в скобках
        #=======================================
        
        modifire_query_string+= request[index_closed_bracket:]   
        #print('the result of __split_request is ---- ',modifire_query_string)
      #  print('the list strings into brackets is -------- ',list_strings_into_brackets)  
        list_result = self.__starting_split(modifire_query_string)
        
        #for node in list_strings_into_brackets:
        self.__union_request(list_result,list_strings_into_brackets)
        #    print('node is----',node)
       
            
        print(list_result)
        return list_result
             
    def get_SQLRequest (self,user_request):
        '''
            преобразование пользовательского запроса в SQL запрос
        '''
        request = self.__cleare_extra_space(user_request); # строка запроса заданная пользователем 
                                                           # переведена в один регистр и без двойных пробелов  
        request_list = self.__split_request(request)
        string_result = "SELECT * FROM " #необходима функция определение таблиц.
        
        string = self.__convert_to_SQL(request_list)
        #сделать проверку на исключение
        string_result += self._SQLtables[self._index_using_tables.pop(0)]
        #сделать проверку на исключение
        while self._index_using_tables:
            index = self._index_using_tables.pop(0)
            string_result += ', ' + self._SQLtables[index]
        string_result += ' WHERE'
        return string_result + string
    
    def __is_operator (self, string_list):
        '''
            является ли атом оператором
        '''
        for operator in self._operators:
            if string_list == operator:
                return operator
        return 0
    
    def __is_path (self,string):
        '''
            проверка является ли поле пользовательским или системным полем path
        '''
        index = string.find('path')
        index_open = string.find('"')
        if (index_open >=0):
            index_close = string.find('"',index_open+1) # если не найдется ковычки то -1
            if (index > index_open) and (index < index_close): 
                return 1
        else:
            index_open = string.find("'") 
            if (index_open>=0):
                index_close = string.find("'",index_open+1) # если не найдется ковычки то -1
                if (index > index_open) and (index < index_close): 
                    return 1
        return 0
            
    
    def __is_field (self,string):
        '''
            проверка является ли атом полем
        '''
        index=0
        for operator in self._field_words:
            if string.find(operator,0)>=0:
               
                return index+1
            index+=1 
        return 0
    
    def __adding_index_using_table(self,index):
        '''
            добавление текущей таблицы  таблиц
        '''
        print(index)
        try:
            self._index_using_tables.index(index) # если элемент не найден то добавялется нвоый элемент
        except ValueError: 
            self._index_using_tables.append(index)
    
    def __type_definition(self,atom):
        '''
            определение типа атома (тег, поле и т.д.)
        '''
        index_field_words = self.__is_field(atom) 
        if index_field_words:
            index_field_words-=1 # индекс указывающий на ключевое слово для поля был на 1 больше нужного. 
    #        if self.__is_path(atom): 
    #            return self._SQLtables[self._index_using_tables[0]] + '.path'+ self._field_words[index_field_words] + "'" + atom[atom.find(self._field_words[index_field_words])+len('path'):]
    #        else:
            self.__adding_index_using_table(2)
            self.__adding_index_using_table(3)
            return  ' '+ self._table_objs_fields + '.name = поле AND '+ self._table_fields + '.value ' + self._field_words[index_field_words] + ' значение '
        else:
            self.__adding_index_using_table(1)
            return ' '+ self._table_objs_tags + ".tag_name = '" + atom + "'"        
        #return atom
    
    
    def __union_operator_and_atom(self,atom,index_operator):
        '''
            объединение операторов с атомами (операндами)
        '''
        if self.__is_list(atom):
            result = ' ' + self.__convert_to_SQL(atom) + ' '
        else:
            result = ' ' + self.__type_definition(atom) + ' '
        if (index_operator == 0)or(index_operator == 1):
            return  result + self._operators[index_operator]
        elif (index_operator == 2):
            return self._operators[index_operator] + result
        
        
#    @staticmethod
    def __convert_to_SQL(self,request_list):
        '''
            преобразование вспомагательного списока в sql запрос
        '''
        index = 0
        operator = request_list[0]
        result_string =''
        if operator == '()':
           result_string = ' (' + self.__convert_to_SQL(request_list[1]) +') '
        else:               
            for index in range(1,len(request_list)):
                result_string += self.__union_operator_and_atom(request_list[index], self._operators.index(operator))
            result_string = ' ' + self.__cleare_extra_space(result_string).rstrip(operator)
        return result_string
        
  
if __name__=='__main__':
                
    str_request = 'field1=значение and tag1 or tag2 and (tag3 or tag4 and not (tag9 or tag10)) and (tag5 or tag6) or not (tag7 or tag8)'
  
    B = ProcessingRequest()
    
    print(B.get_SQLRequest(str_request))
    
  
    

