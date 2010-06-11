
'''
Created on 02.06.2010

@author: valexl
'''
#import cPickle as pickle
from RepoManager.SystemInfo import SystemInfo
import os
import pickle

class NeuralNetwork(object):
    '''
    класс нейронной сети, для умного поиска
    '''
    class ExceptionNeuralNetwork(Exception):
        pass
    class ExceptionExistTag(ExceptionNeuralNetwork):
        pass
    class ExceptionNoExistTag(ExceptionNeuralNetwork):
        pass
    class ExceptionExistFile(ExceptionNeuralNetwork):
        pass
    class ExceptionNoExistFile(ExceptionNeuralNetwork):
        pass
    
#    class NeuralData(object):
#        def __init__(self):
#            self.tags=[]
#            self.files=[]
#            self.neural_net = []
#        
#        def load_neuralnet(repo_path,tags):
#            '''
#                загрузить ту часть нейросети, которая содержит данные теги
#            '''
#            pass
#        
#        def save_neuralnet(repo_path):
#            '''
#                сохранить текущее состояние нейросетии
#            '''
#            pass
#    
    def __init__(self):
        '''
            инициализация начальных параметров сети 
        '''
        
        self.tags=[]
        self.files=[]
        self._level_tags=self.tags
        self.neural_net = []
        for i in range(len(self.tags)):
            self.neural_net.append([])
            for j in range(len(self.files)):
                self.neural_net[i].append(0)
        
        self.learning_spid = 0.3 #1\count_tag
        self.definition = 0.01
    
         
    def addTag(self,new_tag):
        '''
            добавление тега в сеть (новых входящих данных)
        '''
        for tag in self.tags:
            if tag==new_tag:
                raise NeuralNetwork.ExceptionExistTag('тег с таким именем существует в сети')
        self.tags.append(new_tag)
        self.neural_net.append([])
        index = len(self.tags)-1
        for i in range(len(self.files)):
            self.neural_net[index].append(0)
        print(self.neural_net)
        
        
    def addFile(self,new_file):
        '''
            добавления файла в сеть (новых выходящих данных и нейрона в выходной слой)
        '''
        for file in self.files:
            if file==new_file:
                print('файл с таким именем существует в сети')
                #raise NeuralNetwork.ExceptionExistFile('файл с таким именем существует в сети')
                return
                
        self.files.append(new_file)
        for i in range(len(self.tags)):
            self.neural_net[i].append(0)
        print(self.neural_net)
        
        
    def deleteTag(self,del_tag):
        '''
            удаление тега (входных данных)
        '''        
        try:
            index=(self.tags.index(del_tag))
#            print(self.tags)
            del(self.tags[index])
#            print(self.tags)
#            print(self.neural_net)
            del(self.neural_net[index])
#            print(self.neural_net)
        except ValueError:
            raise NeuralNetwork.ExceptionNoExistTag('не найден удаляемый тег')
       
    
    def deleteFile(self,del_file):
        '''
            удаление файла (нейрона выходного слоя с его выходными даннми(файлом))
        '''
        try:
            index=(self.files.index(del_file))
#            print(self.files)
            del(self.files[index])
#            print(self.files)
#            print(self.neural_net)
            for files in self.neural_net:
                del(files[index])
#            print(self.neural_net)
        except ValueError:
            raise NeuralNetwork.ExceptionNoExistFile('не найден удаляемый файл')
        
        
    def tagFile(self,file_name,tag_name):
        '''
            пометка тегом файл. вес от тега к нейрону выходного слоя данного файла помечается как 1.
        '''
        try:
            index_file = (self.files.index(file_name))
        except ValueError as err:
            #raise NeuralNetwork.ExceptionNoExistFile('не найден файл или тег...')
            self.addFile(file_name)
            self.tagFile(file_name, tag_name)
#            print(tag_name)
#            print(self._tags)
        try:
            index_tag = (self.tags.index(tag_name))
            if self.neural_net[index_tag][index_file]<1: #если сеть еще не достаточно обучена на этот тег, тогда добавляется
                self.neural_net[index_tag][index_file]=1            
        except ValueError as err:
            self.addTag(tag_name)
            self.tagFile(file_name, tag_name)
          
            
    def releaseFileFromTag(self,file_name,tag_name):
        '''
            освобождение файла от тега (вес связи от тега к нейрону файла становится равной 0)
        '''    
        try:
            index_file = self.files.index(file_name)
            index_tag = self.tags.index(tag_name)
            self.neural_net[index_tag][index_file]=0            
        except ValueError as err:
            raise NeuralNetwork.ExceptionNoExistFile('не найден файл или тег...')
            
    
    def __sumWeightNeural(self,file_name,list_tags):
        index_file = self.files.index(file_name)
        raiting=0
        for tag in list_tags:
#            print(tag)
            index_tag= self.tags.index(tag)
            raiting += self.neural_net[index_tag][index_file]
        return raiting
    
    
    def learning(self,file_name,list_tags=None):
        '''
            обучение сети. для конекретного файла и конкретной выборки происходит пересчет рэйтинга.
        '''
        try:
            if list_tags==None:
                list_tags = self.tags
            raiting = self.__sumWeightNeural(file_name, list_tags)
            new_raiting = raiting + 1
            
            print(new_raiting)
            iteration=0
            delta = new_raiting - raiting
            index_file = self.files.index(file_name)
            self.learning_spid = 1/len(list_tags) #оптимальная скорость для конкретного обучения.
            while ((abs(delta)>self.definition ) and (iteration<100)):
                iteration+=1
                for tag in list_tags:
                    index_tag = self.tags.index(tag)
                    #пересчет весов по формуле "старый вес" + delta * "скорость обучения" * "сигнал". В нашем случае сигнал =1
                    self.neural_net[index_tag][index_file] = self.neural_net[index_tag][index_file] + delta*self.learning_spid 
                raiting = self.__sumWeightNeural(file_name, list_tags)
                print('пересчитанный рейтинг на ',iteration,'-й итерации ====',raiting)
                delta = new_raiting - raiting
                print(delta)
            print(self.neural_net)       
                    
        except ValueError:
            raise NeuralNetwork.ExceptionNoExistFile('не найден файл или тег...')
        
    def __sortByRaiting(self,list_files,list_tags):
        '''
            сортировка файлов по рэйтингу
        '''   
        list_sum = []
        for file_name in list_files:
            list_sum.append(self.__sumWeightNeural(file_name, list_tags))
        
        for index in range(len(list_sum)-1):
            max=0
            max_index = index
            for position in range(index+1,len(list_sum)):
                if list_sum[position] >= list_sum[max_index]:
                    max_index = position
            tmp = list_sum[index]
            list_sum[index] = list_sum[max_index]
            list_sum[max_index]=tmp
            
            tmp = list_files[index]
            list_files[index]=list_files[max_index]
            list_files[max_index]=tmp
            
            
        print(list_sum)
        return (list_files,list_sum)
    
        
    def search(self,list_tags=None):
        '''
            возращает упорядоченный по рэйтингу список файлов, помеченных тегами. 
        '''
        if list_tags== None:
            list_tags = self.tags
        files = []
        for index_file in range(len(self.files)):
            for tag in list_tags:
                try:
                    index_tag = self.tags.index(tag)
                    if self.neural_net[index_tag][index_file]>0:
                        files.append(self.files[index_file])
                        break
                except ValueError:
                    print('тег ',tag,' то не найден... наверное просто пропуск и не учитывать его при поиске')
                    pass
        print(files)
        files, neural_raiting = self.__sortByRaiting(files,list_tags)
        print('after sort',files)
        print('neural raiting',neural_raiting)
        return (files,neural_raiting)
class tmp(object):
    
    def __init__(self):
        self.neural_net = NeuralNetwork()
        
    def loadNet(self):
        file_neurla_net = open(os.path.join('/tmp/tmp',SystemInfo.neural_net_file_path),'rb')
        file_neurla_net.seek(0)
        #self.neural_net = NeuralNetwork()
            
        self.neural_net = pickle.load(file_neurla_net)
#        pickle.dump(self.neural_net, file_neurla_net, pickle.HIGHEST_PROTOCOL)
        
    def saveNet(self):
        file_path = os.path.join('/tmp/tmp',SystemInfo.neural_net_file_path)
        print('file_path',file_path)
        file_neurla_net = open(file_path,'wb')
        pickle.dump(self.neural_net, file_neurla_net, pickle.HIGHEST_PROTOCOL) 
        
if __name__ == '__main__':
    obj = NeuralNetwork()
    obj.addFile('file1')
    obj.addFile('file2')
    print(obj.neural_net)
    obj.tagFile('file1', 'tag_name')
    obj.tagFile('file1','tag')
    print(obj.neural_net)
    obj.learning('file2', ('tag_name','tag'))
    obj.search(['tag_name'])
    
    
#    obj = tmp()
#    obj.neural_net.addFile('file1')
#    obj.neural_net.addFile('file2')
#    obj.neural_net.addTag('tag')
#    obj.neural_net.tagFile('file1', 'tag')
#    print(obj.neural_net.neural_net)
#    obj.saveNet()
#    obj.neural_net.addFile('file3')
#    obj2 = tmp()
#    del(obj2.neural_net)
#    obj2.loadNet()
#    #obj2.neural_net.addFile('file4')
#    print('obj2',obj2.neural_net.neural_net)
#    obj.saveNet()
#    obj2.saveNet()
#    obj.loadNet()
#    print(obj.neural_net.neural_net)
    