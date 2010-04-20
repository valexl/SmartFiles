'''
Created on 16.04.2010

@author: valexl
'''

class ProcessingRequest(object):
    
    def __init__(self,user_request): # конструктор класса
        self.operators = ['or','and','not','()'] # операции языка запроса
        
        self.table_objs = 'object'
        self.table_objs_tags = 'objects_tags'
        self.table_objs_fields = 'objects_fields'
        self.table_fields = 'fields'   
        self.SQLtables = [self.table_objs, self.table_objs_tags, self.table_objs_fields, self.table_fields] # имена таблиц которые учавствуют в запросе Базе Данных
        
        self.index_using_tables = [0]
        self.field_words = ['>', '>=', '<>', '=', ':', '<=', '<'] 
        
        #>, >=, <>, =, :, <=, <     - знаки которые указывают поиск по полям
        #path="путь к директории"   - path указывает поиск по директории
        #                            Необходимо отделять ключевое слово path от обычного поля path
        #
    
        self.request = self.cleare_extra_space(user_request); # строка запроса заданная пользователем 
                                                              # переведена в один регистр и без двойных пробелов  
        
        
        
   
            
    def cleare_extra_space (self,string):    
        '''
        преобразование строки запроса : убираются все 2-е,3-е и тд пробелы.
        '''
        
        str_lenght = len(string)
        string = string.replace('  ',' ')
        while (str_lenght != len(string)):
            str_lenght = len(string)
            string = string.replace('  ',' ')
        return string.lower().strip() # убираются пробелы с начало и конца строки
        
    # преобразование строки запроса : убираются все 2-е,3-е и тд пробелы.
    # ========================================
        
        
    def starting_split (self, request): # поиск в запросе операции с наименьшим проритетом и относительно 
                                        # этой операции запускается функция разбиение
        operator = 0
        while operator < 3:
            if request.count(self.operators[operator])>0:
                flag = 1
                return self.split_by_operator(request,operator)
            operator += 1
        return request
    
       
    def split_by_operator (self,request,operator_index):  #для заданной строки отделяются перанды от
                                                    # операций OR/ AND / NOT
        list_result = self.get_spliting_list(request,operator_index)
        operator_index +=1
        while operator_index <3:
            index = 0
            while index<len(list_result):
                if list_result[index].count(self.operators[operator_index]) > 0:
                    list_result[index] = self.split_by_operator(list_result[index], operator_index)
                    
                index+=1
            
            operator_index +=1
        print(list_result)
        return list_result

    def get_spliting_list (self,request, operator_index): #преобразование строки в список из операции и операндов
        list_result= [self.operators[operator_index]]
        if (operator_index == 0) or (operator_index == 1): # для операций AND OR
            list_result+=request.split(self.operators[operator_index])
        #так как операция NOT унарная то она будет отличаться от преобразований AND, OR
        elif (operator_index ==2): # для операции NOT  
            list_result.append(request.split(self.operators[operator_index])[1])
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

   
    def is_list (self, string_list):
        for operator in self.operators:
            if string_list[0] == operator:
                return 1
        return 0
        
    def union_request (self,list_request,request_into_brackets): #объединение результатов в скобках с искомым
        index = 0
        for node in list_request:
            if self.is_list(node):
                self.union_request(node,request_into_brackets)
            elif node.strip() == self.operators[3]: #скобки
                list_request[index] = ['()',request_into_brackets.pop(0)]
                #print('union request-----',list_request[index])
            index += 1
                
        
        
         
    def split_request (self,request):        #представление строкового запроса в виде списка
       
        count_brackets = request.count('(')
        
        index_open_bracket = request.find('(')
        index_closed_bracket = request.find(')',index_open_bracket)
        modifire_query_string = request[:index_open_bracket] # строка запроса которая получается на основе request путем 
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
                list_strings_into_brackets[pos] = self.split_request(list_strings_into_brackets[pos])
                #print(list_strings_into_brackets[pos])  
        #отделение в запросе выражений в скобках
        #=======================================
        
        modifire_query_string+= request[index_closed_bracket:]   
        #print('the result of split_request is ---- ',modifire_query_string)
      #  print('the list strings into brackets is -------- ',list_strings_into_brackets)  
        list_result = self.starting_split(modifire_query_string)
        
        #for node in list_strings_into_brackets:
        self.union_request(list_result,list_strings_into_brackets)
        #    print('node is----',node)
       
            
        print(list_result)
        return list_result
             
    def get_SQLRequest (self):
        request_list = self.split_request(self.request)
        
        string_result = "SELECT file_path FROM object" #необходима функция определение таблиц.
        
        string_result += self.convert_to_SQL(request_list)
        return string_result
    
    def is_operator (self, string_list):
        for operator in self.operators:
            if string_list == operator:
                return operator
        return 0
    
    def is_path (self,string):
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
            
    
    def is_field (self,string):
        index=0
        for operator in self.field_words:
            if string.find(operator,0)>=0:
               
                return index+1
            index+=1 
        return 0
    
    def adding_index_using_table(self,index):
        print(index)
        try:
            self.index_using_tables.index(index) # если элемент не найден то добавялется нвоый элемент
        except ValueError: 
            self.index_using_tables.append(index)
    
    def type_defintion(self,atom):
        
        index_field_words = self.is_field(atom) 
        if index_field_words:
            index_field_words-=1 # индекс указывающий на ключевое слово для поля был на 1 больше нужного. 
    #        if self.is_path(atom): 
    #            return self.SQLtables[self.index_using_tables[0]] + '.path'+ self.field_words[index_field_words] + "'" + atom[atom.find(self.field_words[index_field_words])+len('path'):]
    #        else:
            self.adding_index_using_table(2)
            return ' ' + self.SQLtables[2] + '.field_name '+ self.field_words[index_field_words] + ' значение '
        else:
            self.adding_index_using_table(1)
            return ' '+ self.SQLtables[1] + ".tag_name = '" + atom + "'"
        
        
        
        
        return atom
    
    
    def union_operator_and_atom(self,atom,index_operator):
        if self.is_list(atom):
            result = ' ' + self.convert_to_SQL(atom) + ' '
        else:
            result = self.type_defintion(atom)
        if (index_operator == 0)or(index_operator == 1):
            return  result + self.operators[index_operator]
        elif (index_operator == 2):
            return self.operators[index_operator] + result
        
        
#    @staticmethod
    def convert_to_SQL(self,request_list):
        index = 0
        operator = request_list[0]
        result_string =''
        if operator == '()':
           result_string = ' (' + self.convert_to_SQL(request_list[1]) +') '
        else:               
            for index in range(1,len(request_list)):
                result_string += self.union_operator_and_atom(request_list[index], self.operators.index(operator))
            result_string = self.cleare_extra_space(result_string).rstrip(operator)
        return result_string
        
  
if __name__=='__main__':
                
    str_request = 'field1=значение and tag1 or tag2 and (tag3 or tag4 and not (tag9 or tag10)) and (tag5 or tag6) or not (tag7 or tag8)'
    #str_request = '(tag1 or tag2) and (tag3 or tag4)'
    #str_request = 'tag1 and tag2 and (tag3 and ((()))tag4) and not (tag5)'
    #str_request = 'not tag1 or not tag2 and not (tag3 or tag4)'
    #str_request = 'tag1 or tag2 or tag3 and tag4 or tag5 and not tag8' 
    #print(str_request.split('bbc'))
    #str_request = 'tag1 or tag2 or and tag5'
    B = ProcessingRequest()
    
    
    #B.split_tmp_func(str_request)
    #B.split_by_operator(str_request)
    res = B.split_request(str_request)
    #print(res)
    #res = ['or', 'tag1 ', ['and', ' tag2 ', ['()', ['or', 'tag3 ', ' tag4']], ['()', ['or', 'tag5 ', ' tag6']]], ['not', ' tag7']]
    print('sql = ', B.convert_to_SQL(res))
    
    
    B.convert_to_SQL(str_request)
    #print(res)
    
    #res =  '"path"="C:/Windows"'
    #res =  "h='C:/Windows'"
    #res = 'tag1'
    
    #print(B.type_defintion(res))
    

