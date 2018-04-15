#encode: utf-8
#coding: utf-8


if __name__ == '__main__':
    import sqlite3
    conn = sqlite3.connect('./data.db')
    cursor = conn.cursor()
    sql = "SELECT yyyy,mm,dd FROM A320FM WHERE ata='ATA-21' ORDER BY yyyy,mm,dd ASC"
    cursor.execute(sql)
    LIST = [[],['Jan',0],['Feb',0],['Mar',0],['Apr',0],['May',0],['Jun',0],['Jul',0],['Aug',0],['Sept',0],['Oct',0],['Nov',0],['Dec',0]]
    YYYY = dict()
    MM = dict()
    DD = dict()
    for row in cursor.fetchall():
        yyyy, mm, dd = row
        if yyyy in YYYY:
            YYYY[yyyy] += 1
        else:
            YYYY[yyyy] = 1
        if mm in MM:
            MM[mm] += 1
        else:
            MM[mm] = 1
        if dd in DD:
            DD[dd] += 1
        else:
            DD[dd] = 1
    print(YYYY)
    print(MM)
    print(DD)