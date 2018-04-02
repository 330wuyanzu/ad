# encode: utf-8
# coding: utf-8

import json
import os

def readJSON(path):
    fl = open(path, 'r', encoding="utf8")
    content = fl.read()
    data_dict = json.loads(content)
    fl.close()
    return data_dict

def toCSV(data_dict, savePath):
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

def transfer(drc):
    files = os.listdir(drc)
    for fl in files:
        if fl.endswith('.json'):
            data = readJSON(drc+'/'+fl)
            toCSV(data, drc+'/'+fl+'.csv')

if __name__ == '__main__':
    transfer('./A319')
    transfer('./A320')
    transfer('./A330')
