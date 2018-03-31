# encode:utf-8
# coding:utf-8
import sys
if sys.version_info[0] == 2:
    from __future__ import division

import json

class Airplane(object):
    def __init__(self, reg, jsonfile):
        self.Registry = reg
        jsondata = open(jsonfile,encoding='utf8').read()
        '''
        type: dict()
        {
            "ATA-xx": [yyyymmdd, ...],
            ...
        }
        '''
        self.__data = jsondata
        '''
        type: [ata, ...]
        '''
        self.ATAs = self.__data.keys()
        '''
        type: [(ata, count), ...]
        '''
        self.ATA_Count = []
        self.Total_Count = 0
        for ata in self.ATAs:
            (ata, count) = (ata, len(self.__data[ata]))
            self.ATA_Count.append((ata, count))
            self.Total_Count += count

