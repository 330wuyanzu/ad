# coding: utf-8
# enode: utf-8

import sqlite3
import json
import os

class JsonReader(object):
    def __init__(self, path):
        self.__path = path

    def Read(self):
        fl = open(self.__path, 'r', encoding='utf8')
        content = fl.read()
        data_dict = json.loads(content)
        return data_dict

class CSV(object):
    def __init__(self):
        pass

    def Write(self, data_dict, savePath):
        tmp = open(savePath, 'w', encoding='utf8')
        tmp.write("ATA,yyyy,mm,dd")
        tmp.close()
        tmp = open(savePath, 'a', encoding='utf8')
        for ata in data_dict.keys():
            date_list = data_dict[ata]
            for date in date_list:
                yyyy = str(date)[0:4]
                mm = str(date)[4:6]
                dd = str(date)[6:8]
                rcd = "\n{0},{1},{2},{3}".format(ata,yyyy,mm,dd)
                tmp.write(rcd)
                tmp.flush()
        tmp.close()

    def Json2CSV(self, drc, svp):
        files = os.listdir(drc)
        for fl in files:
            if fl.endswith(".json"):
                data = JsonReader(drc+'/'+fl).Read()
                self.Write(data, svp+'/'+fl+'.csv')

    def Read(self, path):
        fl = open(path, 'r', encoding='utf8')
        #head = fl.readline()
        #headers = head.strip().split(',')
        line = fl.readline().strip()
        while line:
            yield tuple(line.split(','))
            line = fl.readline().strip()
        fl.close()

class DBwriter(object):
    def __init__(self, db='./data.db', table='A320FM', type="A319"):
        self._db = db
        self._table = table
        self._type = type

    def Insert(self, csvsrc):
        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()
        reader =  CSV().Read(csvsrc)
        for line in reader:
            (ata, yyyy , mm, dd) = line
            type = self._type
            plane = "B-" + csvsrc.split('/')[-1][0:4]
            sql = 'INSERT INTO '+self._table+' VALUES ("{0}","{1}","{2}",{3},{4},{5})'
            sql = sql.format(type,plane,ata,yyyy,mm,dd)
            cursor.execute(sql)
            conn.commit()
            print(sql)
        conn.close()

if __name__ == '__main__':
    CSV().Json2CSV('./JSON/A319', './CSV/A319')
    CSV().Json2CSV('./JSON/A320', './CSV/A320')
    CSV().Json2CSV('./JSON/A330', './CSV/A330')
    
    def batch(drc, writer):
        files = os.listdir(drc)
        for fl in files:
            if fl.endswith(".csv"):
                writer.Insert(drc+'/'+fl)

    writer = DBwriter()
    batch('./CSV/A319',writer)
    
    writer = DBwriter(type="A320")
    batch('./CSV/A320',writer)
    
    writer = DBwriter(table="A330",type="A330")
    batch('./CSV/A330',writer)