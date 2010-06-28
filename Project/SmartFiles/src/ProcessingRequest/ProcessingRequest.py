'''
Created on 10.04.2010

@author: valexl
'''
#@staticmethod
def cleareExtraSpace (request):    
        '''
            убираются все удвоенные и начальные пробелы.
        '''
        
        str_lenght = len(request)
        request = request.replace('  ',' ')
        while (str_lenght != len(request)):
            str_lenght = len(request)
            request = request.replace('  ',' ')
         
        return request.lower().strip() # убираются пробелы с начало и конца строки
    
        
    #@staticmethod
def cleareSpaceAboutOperator(request,operator):     
        '''
            убираются пробелы между полем операцией и значением
        '''
        try:
            index=0
            len_operator=len(operator)
            while (index>=0):
                index = request.find(operator,index+1)
                if index>0:                
                    if request[index-1]==' ':
                        request=request[:index-1] + request[index:]
                        index-=1
                    if request[index+len(operator)]==' ':
                        request=request[:index+len(operator)] + request[index+len(operator)+1:]
            return request
        except IndexError:
            raise ProcessingRequest.ExceptionInvalidRequestSyntaxis('не найдено значение поля')
class ProcessingRequest(object):
    '''
        преобразование пользовательского запроса в SQL (В данный момент не учтены пользователи, path)
    '''
    class ExceptionProcessingRequest(Exception):
        pass
    class ExceptionInvalidRequestSyntaxis(ExceptionProcessingRequest):
        pass 
    _operators = [' or ',' and ',' not ','()'] # операции языка запроса
        
    _table_objs = 'entity'
    _table_objs_tags = 'entity_tags'
    _table_objs_fields = 'entity_fields'
    _table_fields = 'fields'   
    _SQLtables = [_table_objs,_table_objs_tags,_table_objs_fields] # имена таблиц которые учавствуют в запросе Базе Данных
    _using_table = []
    _field_words = ['<>','<=', '>=','>' , '=', ':', '<'] 
    
        
        #>, >=, <>, =, :, <=, <     - знаки которые указывают поиск по полям
        #path="путь к директории"   - path указывает поиск по директории
        #                            Необходимо отделять ключевое слово path от обычного поля path
        #
    
        #self.request = '' 
        #self.cleareExtraSpace(user_request); # строка запроса заданная пользователем 
                                                              # переведена в один регистр и без двойных пробелов  
        
    


        
    @staticmethod  
    def __startingSplit ( request): 
        '''
        поиск в запросе операции с наименьшим проритетом и относительно
        этой операции запускается функция разбиение     
        '''
        index_operator = 0
        while index_operator < 3:
            if request.count(ProcessingRequest._operators[index_operator])>0:
                flag = 1
                return ProcessingRequest.__splitByOperator(request,index_operator)
            index_operator += 1
        return [request]
    
    @staticmethod
    def __splitByOperator (request,operator_index):
        '''
          для заданной строки отделяются операнды от операций OR/ AND / NOT
                                                    
        '''
        list_result = ProcessingRequest.__getSplitingList(request,operator_index)
#        print(list_result)
        operator_index +=1
        while operator_index <3:
            index = 0
            while index<len(list_result):
                if list_result[index].count(ProcessingRequest._operators[operator_index]) > 0:
                    list_result[index] = ProcessingRequest.__splitByOperator(list_result[index], operator_index)
                    
                index+=1
            
            operator_index +=1
        
        return list_result
    @staticmethod
    def __getSplitingList (request, operator_index):
        '''
        
        преобразование строки в список из операций и операндов
        
        '''
        list_result= [ProcessingRequest._operators[operator_index]]
        if (operator_index == 0) or (operator_index == 1): # для операций AND OR
            list_result+=request.split(ProcessingRequest._operators[operator_index])
        #так как операция NOT унарная то она будет отличаться от преобразований AND, OR
        elif (operator_index ==2): # для операции NOT  
            list_result.append(request.split(ProcessingRequest._operators[operator_index])[1])
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
    #            Реализован 1й способ решения.

    @staticmethod
    def __isList ( atom):
        '''
        проверка элемента является ли он списком или нет
        '''
        for operator in ProcessingRequest._operators:
            if atom[0] == operator:
                return 1
        return 0
    
    @staticmethod    
    def __unionRequest (list_request,request_into_brackets):
        '''
         объединение результатов в скобках с искомым
        '''
        index = 0
        for node in list_request:
            if ProcessingRequest.__isList(node):
                ProcessingRequest.__unionRequest(node,request_into_brackets)
            elif node.strip() == ProcessingRequest._operators[3]: #скобки
                list_request[index] = ['()',request_into_brackets.pop(0)]
                #print('union request-----',list_request[index])
            index += 1
        
    @staticmethod        
    def __splitRequest (request):       
        '''
         представление строкового запроса в виде вспомогательного списка
        '''       
        count_brackets = request.count('(')
        
        index_open_bracket = request.find('(')
        index_closed_bracket = request.find(')',index_open_bracket)
        modifide_query_string = request[:index_open_bracket] # копирование всего запроса до скобок.
        
                                                            #PS модифицированная строка запроса в процессе выполнение процедурры 
                                                            #получается на основе request путем 
                                                            # вырезания содержимого скобок. Т.е. вместо "(запрос)" 
                                                            #остаются только "()"
                                                            
                                                                        
        list_strings_into_brackets = []  
        #======================================
        #отделение в запросе выражений в скобках
        if count_brackets > 0:
            modifide_query_string+='('
                          
            index = index_open_bracket
            count_brackets-=1
            while count_brackets > 0 :
                count_brackets -=1
                index = request.find('(',index+1)
                if index > index_closed_bracket:
                    modifide_query_string+= request[index_closed_bracket:index+1]
                    list_strings_into_brackets.append(request[index_open_bracket+1:index_closed_bracket])
                    index_open_bracket = index
                    index_closed_bracket = request.find(')',index_open_bracket)
                else:
                    index_closed_bracket = request.find(')',index_closed_bracket+1)
            list_strings_into_brackets.append(request[index_open_bracket+1:index_closed_bracket])
            for pos in range(len(list_strings_into_brackets)):
                list_strings_into_brackets[pos] = ProcessingRequest.__splitRequest(list_strings_into_brackets[pos])
                #print(list_strings_into_brackets[pos])  
        #отделение в запросе выражений в скобках
        #=======================================
        
        modifide_query_string+= request[index_closed_bracket:]  

        list_result = ProcessingRequest.__startingSplit(modifide_query_string)
        #print('list_result',list_result)
        
        #for node in list_strings_into_brackets:
        ProcessingRequest.__unionRequest(list_result,list_strings_into_brackets)
        #    print('node is----',node)
       
            
        
        return list_result
    #=======================

    @staticmethod
    def __convertToSQL(user_request_list,flag=True):
        #index = 0
#        print('convertToSQL user_request_list',user_request_list)
        item = ProcessingRequest.__isOperator(user_request_list[0])
#        print('operator is',item)
        
        result_string =''
        if item == '()':
           result_string = ' (' + ProcessingRequest.__convertToSQL(user_request_list[1],False) +') '
        elif item == ' and ': 
            index = 2
            result_string = ProcessingRequest.__convertToSQL(user_request_list[1],False)    
            while index < len(user_request_list):
                result_string += ' AND entity.id IN ( ' + ProcessingRequest.__startConvertToSQL(user_request_list[index],0) + ')'
                index+=1
        elif item==' or ':
            index = 2
            result_string = ProcessingRequest.__convertToSQL(user_request_list[1],False)
            while index < len(user_request_list):
                result_string +=' or ' + ProcessingRequest.__convertToSQL(user_request_list[index],False)
                index+=1
        else:
            result_string=ProcessingRequest.__typeDefinition(user_request_list)
            #result_string=ProcessingRequest.__typeDefinition(item)
#        print('используемые таблицы', ProcessingRequest._using_table)
        if flag:
#            print(ProcessingRequest._using_table)
            tables=''
            for table in ProcessingRequest._using_table:
                tables+= ', ' + table             
            result_string = tables + " WHERE " + result_string 
        return result_string

    @staticmethod
    def __startConvertToSQL(user_request_list, flag=1):
        
        if flag:
            result = ' SELECT DISTINCT entity.id, entity.title, entity.neuralnet_raiting, entity.object_type, entity.file_path FROM entity'
        else:
            result = ' SELECT DISTINCT entity.id FROM entity '
        
        
        result += ProcessingRequest.__convertToSQL(user_request_list)
        #print(result)

        return result
    #======================
    @staticmethod         
    def getSQLRequest (user_request,is_neural_net=False):
        '''
            преобразование пользовательского запроса в SQL запрос
        '''
        try:
            request = cleareExtraSpace(user_request); # строка запроса заданная пользователем 
                                                               # переведена в один регистр и без двойных пробелов
            for operator in ProcessingRequest._field_words: 
                request = cleareSpaceAboutOperator(request,operator)
            
            
            
            request_list = ProcessingRequest.__splitRequest(request)
            
                
            if len(request_list)==1:
                result_sql_request = ProcessingRequest.__startConvertToSQL(request_list[0]) 
            else:
                result_sql_request = ProcessingRequest.__startConvertToSQL(request_list)
            
            if is_neural_net:
                result_sql_request += ' ORDER BY entity.neuralnet_raiting DESC'
            return result_sql_request
        except IndexError as error:
            print(error)
            raise ProcessingRequest.ExceptionInvalidRequestSyntaxis('не найдено значение поля')

    @staticmethod
    def __isOperator ( atom):
        '''
            является ли атом оператором.
            возращает 0 в случае неудачи 
            или оператор в случае успеха
        '''
        for operator in ProcessingRequest._operators:
            if atom == operator:
                return operator
        return 0
        
    @staticmethod
    def __isField (atom):
        '''
            проверка является ли атом полем. 
            Если не поле то возращается 0 индекс оператора +1 
        '''
#        print('is field? ---- ',atom)
        for operator in ProcessingRequest._field_words:
            if atom.find(operator,0)>=0:
                return operator
        return 0
    

    
    @staticmethod
    def __typeDefinition(atom):
        '''
            определение типа атома (тег, поле и т.д.)
        '''
        field_operator = ProcessingRequest.__isField(atom) 
        if field_operator:
            field_name, field_value = atom.split(field_operator)
            field_name = field_name.strip()
            try:
                ProcessingRequest._using_table.index(ProcessingRequest._table_objs_fields)
            except ValueError:
                ProcessingRequest._using_table.append(ProcessingRequest._table_objs_fields)
            return  ' '+ ProcessingRequest._table_objs_fields + ".field_name = '" + field_name + "' AND "+ ProcessingRequest._table_objs_fields + '.value ' + field_operator + " '" + field_value + "'" + ' AND ' + ProcessingRequest._table_objs +".id=" + ProcessingRequest._table_objs_fields + ".entity_id"
        else:
            atom = atom.strip()
            try:
                ProcessingRequest._using_table.index(ProcessingRequest._table_objs_tags)
            except ValueError:
                ProcessingRequest._using_table.append(ProcessingRequest._table_objs_tags)
            return ' '+ ProcessingRequest._table_objs_tags + ".tag_name = '" + atom + "'" + ' AND ' + ProcessingRequest._table_objs +".id=" + ProcessingRequest._table_objs_tags + ".entity_id"        

    

  
if __name__=='__main__':
                
    str_request = 'aa and (torion and (cc or ee) or field=value)'
    per=ProcessingRequest.getSQLRequest(str_request)
    
    print('the result is ----')
    print(per)
    

