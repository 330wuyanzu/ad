# encode:utf-8
# coding:utf-8


import sqlite3
import json
import os

if __name__ == '__main__':
    def DecendSort(tuple_list):
        endindex = len(tuple_list) - 1
        while True:
            if endindex < 1:
                break            
            index = 0                
            while True:
                left = tuple_list[index]
                right = tuple_list[index+1]
                if left[1] < right[1]:
                    left, right = right, left
                    tuple_list[index] = left
                    tuple_list[index+1] = right
                index += 1
                if index == endindex:
                    break
            endindex -= 1
        return tuple_list
    # 统计没一架飞机的故障数量
    def ForPlane(table, plane, deadline):
        conn = sqlite3.connect('./data.db')
        cursor = conn.cursor()
        sql = 'SELECT ata FROM {0} WHERE plane="{1}"'.format(table, plane)
        cursor.execute(sql)
        total = 0
        tmp = dict()
        for row in cursor.fetchall():
            total += 1
            (ata,) = row
            if ata in tmp:
                tmp[ata] += 1
            else:
                tmp.update({ata:1})
        conn.close()
        tmp_list = []
        for ata, count in tmp.items():
            tmp_list.append((ata, count, count/total))
        _sorted = DecendSort(tmp_list)
        data = {
            "Airplane": plane,
            "Deadline": deadline,
            "Total": total,
            "ATA": _sorted
        }
        meta = json.dumps(data)
        path = './data/{0}.js'.format(plane.replace('-',''))
        fl = open(path, 'w', encoding='utf8')
        meta = 'const {0} = {1};'.format(plane.replace('-',''), meta)
        fl.write(meta)
        fl.close()
    # 统计320机队的总体数量
    def ForFM(table, fm, deadline):
        conn = sqlite3.connect('./data.db')
        cursor = conn.cursor()
        sql = 'SELECT ata FROM %s'%table
        cursor.execute(sql)
        total = 0
        tmp = dict()
        for row in cursor.fetchall():
            total += 1
            (ata,) = row
            if ata in tmp:
                tmp[ata] += 1
            else:
                tmp.update({ata:1})
        conn.close()
        tmp_list = []
        for ata, count in tmp.items():
            tmp_list.append((ata, count, count/total))
        _sorted = DecendSort(tmp_list)
        data = {
            "Family": fm,
            "Deadline": deadline,
            "Total": total,
            "ATA": _sorted
        }
        meta = json.dumps(data)
        path = './data/%s.js'%fm
        fl = open(path, 'w', encoding='utf8')
        meta = 'const {0} = {1};'.format(fm, meta)
        fl.write(meta)
        fl.close()
    # 统计330机队的总体数量
    ForPlane('A320FM', 'B-6425', '2018-03-30')
    ForFM('A320FM', 'A320', '2018-03-30')
    ForFM('A330', 'A330', '2018-03-30')