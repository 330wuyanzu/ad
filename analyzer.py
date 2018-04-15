# encode:utf-8
# coding:utf-8


import sqlite3
import json
import os

class Fleet(object):
    def __init__(self, db, model):
        self._db = db
        self._total = 0
        self._type = model
        self._ata_count = self._countATA()
        # 降序排列每个章节的故障量 [[ATA,count],......]
        self._sorted_ata = self._decendSort(self._ata_count.items())
        self._max = self._sorted_ata[0][0]
        (y,m,d) = self._countMAX()
        self._y_max = y
        self._m_max = m
        self._d_max = d
        self._sorted_yy = self._decendSort(self._y_max.items(), pos=0)
        self._sorted_mm = self._decendSort(self._m_max.items(), pos=0)
        self._sorted_dd = self._decendSort(self._d_max.items(), pos=0)
        
    @property
    def YYYY(self):
        self._sorted_yy.reverse()
        return self._sorted_yy

    @property
    def SortedMM(self):
        self._sorted_mm.reverse()
        return self._sorted_mm

    @property
    def SortedDD(self):
        self._sorted_dd.reverse()
        return self._sorted_dd
    
    @property
    def MaxOne(self):
        return self._max

    @property
    def Model(self):
        return self._type

    @property
    def Total(self):
        return self._total

    @property
    def SortedATA(self):
        return self._sorted_ata

    def Write(self, deadline):
        _data = {
            'update': deadline,
            'total': self.Total,
            'ATA': self.SortedATA,
            'MAX': self.MaxOne,
            'YEAR': self.YYYY,
            'MONTH': self.SortedMM,
            'DAY': self.SortedDD
        }
        _data = json.dumps(_data)
        _path = './data/{0}.js'.format(self._type)
        _meta = 'const {0}={1};'.format(self._type, _data)
        _fl = open(_path, 'w', encoding='utf8')
        _fl.write(_meta)
        _fl.close()

    def _countATA(self):
        _conn = sqlite3.connect(self._db)
        _cursor = _conn.cursor()
        _sql = 'SELECT ata FROM {0} ORDER BY ata ASC'.format(self.Model)
        _cursor.execute(_sql)
        _rt = {}
        for row in _cursor.fetchall():
            (ata,) = row
            self._total += 1
            if ata in _rt:
                _rt[ata] += 1
            else:
                _rt.update({ata:1})
        _conn.close()
        return _rt

    def _decendSort(self, what, pos=1):
        _lst = list(what)
        _end = len(_lst)-1
        while _end >= 1:
            _index = 0
            while _index < _end:
                LT = _lst[_index]
                RT = _lst[_index+1]
                if LT[pos] < RT[pos]:
                    _lst[_index], _lst[_index+1] = RT, LT
                _index += 1
            _end -= 1
        _rt = []
        for item in _lst:
            _rt.append(list(item))
        return _rt

    def _countMAX(self):
        _conn = sqlite3.connect(self._db)
        _cursor = _conn.cursor()
        _sql = "SELECT yyyy,mm,dd FROM {0} WHERE ata='{1}' ORDER BY yyyy,mm,dd ASC".format(self.Model,self.MaxOne)
        _cursor.execute(_sql)
        YY = {}
        MM = {}
        DD = {}
        for row in _cursor.fetchall():
            (yyyy,mm,dd) = row
            if yyyy in YY:
                YY[yyyy] += 1
            else:
                YY.update({yyyy:1})
            if mm in MM:
                MM[mm] += 1
            else:
                MM.update({mm:1})
            if dd in DD:
                DD[dd] += 1
            else:
                DD.update({dd:1})
        return (YY,MM,DD)

class A320FM(Fleet):
    pass

class A330(Fleet):
    pass

if __name__ == '__main__':
    A320 = A320FM('./data.db','A320FM')
    
    A320.Write('2018-03-30')

    print('Model: %s'%A320.Model)
    print('Max ATA: %s'%A320.MaxOne)
    for item in A320.SortedATA:
        print('Sorted ATA: {0}'.format(item))
    for item in A320.YYYY:
        print('Sorted YEAR: {0}'.format(item))
    for item in A320.SortedMM:
        print('Sorted MONTH: {0}'.format(item))
    for item in A320.SortedDD:
        print('Sorted DAY: {0}'.format(item))
    