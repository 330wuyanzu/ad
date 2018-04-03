# encode: utf-8
# coding: utf-8

import sqlite3
import os

class CSVreader(object):
    def __init__(self, path):
        self.__firstline = ''
        self.__file = path
        self.Headers = []

    def Read(self):
        fl = open(self.__file,'r',encoding='utf8')
        head = fl.readline()
        headers = head.strip().split(',')
        self.Headers = tuple(headers)
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
        reader =  CSVreader(csvsrc)
        for line in reader.Read():
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
    def batch(drc, writer):
        files = os.listdir(drc)
        for fl in files:
            if fl.endswith(".csv"):
                writer.Insert(drc+'/'+fl)

    writer = DBwriter()
    batch('./A319',writer)
    
    writer = DBwriter(type="A320")
    batch('./A320',writer)
    
    writer = DBwriter(table="A330",type="A330")
    batch('./A330',writer)
