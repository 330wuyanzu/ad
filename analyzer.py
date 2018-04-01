# encode:utf-8
# coding:utf-8


import json
import os

class Airplane(object):
    def __init__(self, reg, jsonfile, deadline):
        self.Registry = reg
        self.Deadline = deadline
        jsondata = open(jsonfile,encoding='utf8').read()
        '''
        type: dict()
        {
            "ATA-xx": [yyyymmdd, ...],
            ...
        }
        '''
        self.__data = json.loads(jsondata)
        '''
        type: [ata, ...]
        '''
        self.ATAs = self.__data.keys()
        '''
        type: [(ata, count), ...]
        '''
        self.Total_Count = 0
        self.ATA_Digit = []
        
        ata_count = []
        for ata in self.ATAs:
            (ata, count) = (ata, len(self.__data[ata]))
            ata_count.append((ata, count))
            self.Total_Count += count
        for (ata, count) in ata_count:
            (ata, count, ratio) = (ata, count, count/self.Total_Count)
            self.ATA_Digit.append((ata, count, ratio))
        
    def __decendSort(self):
        endindex = len(self.ATA_Digit)-1
        while True:
            if endindex < 1:
                break            
            index = 0                
            while True:
                left = self.ATA_Digit[index]
                right = self.ATA_Digit[index+1]
                if left[1] < right[1]:
                    left, right = right, left
                    self.ATA_Digit[index] = left
                    self.ATA_Digit[index+1] = right
                index += 1
                if index == endindex:
                    break
            endindex -= 1


    def ForSerial(self):
        self.__decendSort()
        serial = {
            "Airplane": self.Registry,
            "Deadline": self.Deadline,
            "Total": self.Total_Count,
            "ATA": self.ATA_Digit
        }
        return serial

    def SaveResult(self, path):
        fullpath = path+"/"+self.Registry+".json"
        fl = open(fullpath, 'w',encoding='utf8')
        fl.write(json.dumps(self.ForSerial()))
        fl.close()

    def __str__(self):
        _1 = "Airplane: "+self.Registry
        _2 = "Statics Time: "+self.Deadline
        _3 = "Total Malfunction: "+str(self.Total_Count)
        tmp = _1+'\n'+_2+'\n'+_3+'\n'
        for (ata, count, ratio) in self.ATA_Digit:
            tmp += ata +": "+"count - "+str(count)+"  ratio - "+str(ratio)+"\n"
        return tmp


if __name__ == '__main__':
    data_list = []
    for (d,sub,files) in os.walk('./A319'):
        for fl in files:
            path = d+'/'+fl
            reg = "B-"+fl[0:4]
            data_list.append(Airplane(reg, path, '2018-03-30').ForSerial())
    for (d,sub,files) in os.walk('./A320'):
        for fl in files:
            path = d+'/'+fl
            reg = "B-"+fl[0:4]
            data_list.append(Airplane(reg, path, '2018-03-30').ForSerial())
    for (d,sub,files) in os.walk('./A330'):
        for fl in files:
            path = d+'/'+fl
            reg = "B-"+fl[0:4]
            data_list.append(Airplane(reg, path, '2018-03-30').ForSerial())

    fl = open('./data.js','w', encoding='utf8')
    data = json.dumps(data_list)
    stam = 'const DATA = '+data
    fl.write(stam)
    fl.close()
    