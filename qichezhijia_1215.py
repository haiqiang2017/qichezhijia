# _*_ ecoding:utf-8 _*_
import sys
import os
import requests
import time
import urllib
import argparse
import xlrd
import csv
from xlutils.copy import copy
from multiprocessing.dummy import Pool
reload(sys)
sys.setdefaultencoding('utf8')
import json

sessdown = requests.Session()


def makedirs_p(dest):
    if not os.path.exists(dest):
        try:
            os.makedirs(dest)
        except OSError, ex:
            if 'File exists' in ex:
                pass
            else:
                raise
def is_exists(chekuan,loc,year,dic_che):
    for key, value in dic_che.items():
        if chekuan in key and loc in key and year in key:
            return key,value
        else:
           continue
    return 0
def step1 (dic_che):
    header = []
    num = 0
    outpath = '/Users/haiqiang/Desktop/qichezhijia/target.xlsx'
    '''
    num = 0
    for key,value in dic_che.items():
        if str(key).startswith(','):
            continue
        try:
            num = num + 1
            print num,key,value
        except:
            continue
    '''
    data = xlrd.open_workbook(outpath)
    table = data.sheet_by_index(0)
    nrows = table.nrows
    result = []
    for row in range(nrows):
        if str(table.row_values(row)[3]).startswith('格灵'):
            continue
        #try:
        try:
            chekuan = table.row_values(row)[3].split('-')[0]
            loc = table.row_values(row)[3].split('-')[1]
            year = table.row_values(row)[3].split('-')[2]
        except Exception as e:
            print e
            continue
        dic_row = {}
        #用于存储每行的字典类型
        if is_exists(chekuan,loc,year,dic_che):
            key,value1 = is_exists(chekuan,loc,year,dic_che)
            dic_che.pop(key)
            dic_row['汽车之家名称'] = key
            for col in range(0,69,1):
                attr = str(table.row_values(0)[col]).split('（')[0]
                if col < 4 or col == 5:
                    dic_row[attr] = table.row_values(row)[col]
                elif col == 4:
                    continue
#                attr = table.row_values(0)[col].split('（')[0]
                else:
                    if value1.has_key(attr):
                        if not value1[attr]:
                            dic_row[attr] = '空'
                            continue
#                        print attr,'haha',value1[attr]
                        dic_row[attr] = value1[attr]
                    else:
                        dic_row[attr] = '-'
            result.append(dic_row)
        else:
            for col in range(0, 69, 1):
                attr = str(table.row_values(0)[col]).split('（')[0]

                if col < 4 or col == 5:
                    dic_row[attr] = table.row_values(row)[col]
                else:
                    dic_row[attr] = '-'
            result.append(dic_row)
    tmp = []
    with open('no_match.txt', 'w') as load_w:
        for k,v in dic_che.items():
            v['未匹配汽车之家名称']=k
            print json.dumps(v, encoding="UTF-8", ensure_ascii=False)
            load_w.write(str(json.dumps(v, encoding="UTF-8", ensure_ascii=False)) + '\n')
    #for item in result[0].keys():
    #    header.append(item)

    #csvFile = open("no_match.csv", "w")
    #dict_writer = csv.DictWriter(csvFile, header)
    #dict_writer.writeheader()
    #dict_writer.writerows(result)#
    #csvFile.close()
def step2(dic_che):
    result = []
    for k,v in dic_che.items():
        v['汽车之家名称']=k
        result.append(v)
    with open('quchong.txt','w') as load_w:
        for i in result:
            print json.dumps(i, encoding="UTF-8", ensure_ascii=False)
            load_w.write(str(json.dumps(i, encoding="UTF-8", ensure_ascii=False))+'\n')
def convert_dic_csv(result):
    header = []
    for item in result[0]:
        print item
        header.append(item)
#    print header
    csvFile = open("quchong.csv", "w")
    dict_writer = csv.DictWriter(csvFile, header)
    dict_writer.writeheader()
    dict_writer.writerows(result)
    csvFile.close()



if __name__ == "__main__":
    source='/Users/haiqiang/Desktop/qichezhijia/attribute.txt'
    dic_che = {}
    #用于存储字典的中间结果
    dic_tmp = {}
    i = 0
    same = ''
    max = 0
    #定义一个列表用于后续存储最终结果
    result = []
    with open(source,'r+') as load_r:
        for line in load_r.readlines():
            try:
                dic_att = {}
                i = i + 1
                chekuan = line.strip().split(' ')[0]
                if not chekuan:
                    continue
                che = chekuan.split('/2')[0]
                if che != same:
                    #如果当前的车和上一个不相同，则表示上一轮的最后一个字典是符合条件的字典
                    dic_che[chekuan]= dic_tmp
                    same = che
                    max = 0
                che_attr = line.split(',',1)[1].strip()
                #生成小字典
                for dic in che_attr.split(','):
                    key = dic.split(':')[0].split('(')[0]
                    if '行程' in key:
                        key = '行程'
                    if '工信部工信部综合油耗' in key:
                        key = '工信部工信部综合油耗'
                    if '油箱容积' in key:
                        key = '油箱容量'
                    if '实测油耗' in key:
                        key = '实际油耗'
                    if key.startswith('#'):
                        key = key.split('#')[1]
                #    if '#缸盖材料' in key:
                #        key = '缸盖材料'
                #    if '#车体结构' in key:
                 #       key = '车体结构'
                    if '上市' in key:
                        key = '上市时间'
                    if '挡位个数' in key:
                        key = '档位个数'
                    if '工信部纯电续驶里程' in key:
                        key = '工信部纯电里程'
                    if '整车质保' in key:
                        key = '整车质量'
                    if '整备质保' in key:
                        key = '整备质量'
                    value = dic.split(':')[1]
                    if value == '-':
                        value = 0
                    dic_att[key]=value

                if not dic_att.has_key('燃油标号'):
                    continue
    #            if dic_att['工信部']=='-':
    #                continue
                if float(dic_att['燃油标号'])>=max:
                    max = float(dic_att['燃油标号'])
                    dic_tmp = dic_att
                else:
                    continue
            except Exception as e:
                continue

    step1(dic_che)










