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
# 该函数用于精准匹配，必须主品牌，子品牌和年款都匹配
def is_exists(car_type,dic_che):
    try:
        chekuan = car_type.split('-')[0]
        loc = car_type.split('-')[1]
        if '(' in loc:
            loc = loc.split('(')[0]
        if '&' in loc:
            loc = loc.split('&')[1]
        if '_' in loc:
            loc = loc.split('_')[0]
        year = car_type.split('-')[2]
        if '_' in  year:
           year = year.split('_')[-1]
        if '&' in year:
            year = year.split('&')[1]
        for key, value in dic_che.items():
            if chekuan in key and loc in key and year in key:
                return key,value
            else:
               continue
        return 0
    except Exception as e:
        print e
#该函数为主品牌和子品牌匹配成功 年款不匹配
def year_not_exists(car_type,dic_che):
    try:
        chekuan = car_type.split('-')[0]
        loc = car_type.split('-')[1]
        if '(' in loc:
            loc = loc.split('(')[0]
        if '&' in loc:
            loc = loc.split('&')[1]
        if '_' in loc:
            loc = loc.split('_')[0]
        year = car_type.split('-')[2]
        if '_' in  year:
           year = year.split('_')[-1]
        if '&' in year:
            year = year.split('&')[1]
        for key, value in dic_che.items():
            if chekuan in key and loc in key and year not in key:
                return key,value
            else:
               continue
        return 0
    except Exception as e:
        print e

#该函数用于子品牌匹配，其他信息不匹配
def zi_exists(car_type,dic_che):
    try:
        chekuan = car_type.split('-')[0]
        loc = car_type.split('-')[1]
        if '(' in loc:
            loc = loc.split('(')[0]
        if '&' in loc:
            loc = loc.split('&')[1]
        if '_' in loc:
            loc = loc.split('_')[0]
        year = car_type.split('-')[2]
        if '_' in  year:
           year = year.split('_')[-1]
        if '&' in year:
            year = year.split('&')[1]
        for key, value in dic_che.items():
            if chekuan not in key and loc in key and year not in key:
                return key,value
            else:
               continue
        return 0
    except Exception as e:
        print e
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
    num = 0
    num_year = 0
    num_zi = 0
    result = []
    for row in range(nrows):
        if str(table.row_values(row)[3]).startswith('格灵'):
            continue
        #try:
        try:
            car_type = table.row_values(row)[3]
            #chekuan = table.row_values(row)[3].split('-')[0]
            #loc = table.row_values(row)[3].split('-')[1]
            #year = table.row_values(row)[3].split('-')[2]
            #if '_' in  table.row_values(row)[3]:
            #    style = table.row_values(row)[3].split('_')[-1]
        except Exception as e:
            print e
            continue
        dic_row = {}
        #用于存储每行的字典类型
        if is_exists(car_type,dic_che):
            num += 1
            key,value1 = is_exists(car_type,dic_che)
        #    dic_che.pop(key)
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
        #elif year_not_exists(car_type,dic_che):
        #    num_year += 1
        #    key, value1 = year_not_exists(car_type, dic_che)
        #    #    dic_che.pop(key)
        #    dic_row['汽车之家名称'] = str(key)+'年款不匹配'
        #    for col in range(0, 69, 1):
        #        attr = str(table.row_values(0)[col]).split('（')[0]
        #        if col < 4 or col == 5:
        #            dic_row[attr] = table.row_values(row)[col]
        #        elif col == 4:
        #            continue
        #            #                attr = table.row_values(0)[col].split('（')[0]
        #        else:
        #            if value1.has_key(attr):
        #                if not value1[attr]:
        #                    dic_row[attr] = '空'
        #                    continue
        #                    #                        print attr,'haha',value1[attr]
        #                dic_row[attr] = value1[attr]
        #            else:
        #                dic_row[attr] = '-'
        #    result.append(dic_row)
        #elif zi_exists(car_type,dic_che):
        #    num_zi += 1
        #    key, value1 = zi_exists(car_type, dic_che)
        #    #    dic_che.pop(key)
        #    dic_row['汽车之家名称'] = str(key)+'只有子品牌匹配'
        #    for col in range(0, 69, 1):
        #        attr = str(table.row_values(0)[col]).split('（')[0]
        #        if col < 4 or col == 5:
        #            dic_row[attr] = table.row_values(row)[col]
        #        elif col == 4:
        #            continue
        #            #                attr = table.row_values(0)[col].split('（')[0]
        #        else:
        #            if value1.has_key(attr):
        #                if not value1[attr]:
        #                    dic_row[attr] = '空'
        #                    continue
        #                    #                        print attr,'haha',value1[attr]
        #                dic_row[attr] = value1[attr]
        #            else:
        #                dic_row[attr] = '-'
        #    result.append(dic_row)
        else:
            for col in range(0, 69, 1):
                attr = str(table.row_values(0)[col]).split('（')[0]

                if col < 4 or col == 5:
                    dic_row[attr] = table.row_values(row)[col]
                else:
                    dic_row[attr] = '-'
            result.append(dic_row)
    print num,num_year,num_zi
    tmp = []
    #for k,v in dic_che.items():
    #    v['未匹配汽车之家名称']=k
    #    tmp.append(v)
    #for item in tmp[0].keys():
    #    header.append(item)
    for item in result[0].keys():
        header.append(item)

    csvFile = open("instance.csv", "w")
    dict_writer = csv.DictWriter(csvFile, header)
    dict_writer.writeheader()
    dict_writer.writerows(result)
    csvFile.close()
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
    source='/Users/haiqiang/Desktop/qichezhijia/all.txt'
    dic_che = {}
    #用于存储字典的中间结果
    dic_tmp = {}
    i = 0
    cal = 0
#    same = ''
    same = []
    max = 0
    #定义一个列表用于后续存储最终结果
    result = []
    with open(source,'r+') as load_r:
        for line in load_r.readlines():
            try:
                dic_att = {}
                i = i + 1
                chekuan = line.strip().split(',')[0]
                if not chekuan:
                    continue
        #        che = chekuan.split('/2')[0]
            #    print chekuan
                if chekuan not in same:
                    #如果当前的车和上一个不相同，则表示上一轮的最后一个字典是符合条件的字典
                    same.append(chekuan)
                    max = 0
            #        dic_che[chekuan]= dic_tmp
                    che_attr = line.split(',',1)[1].strip()
                    #生成小字典
                    for dic in che_attr.split(','):
                        key = dic.split(':')[0].split('(')[0]
                        if '行程' in key:
                            key = '行程'
                        if '工信部综合油耗' in key:
                            key = '工信部综合油耗'
                        if '油箱' in key:
                            cal += 1
                            print cal,key,dic.split(':')[1]
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
                        if  key == '标':
                            key = '燃油标号'
                        value = dic.split(':')[1]
                        if value == '-':
                            value = 0
                        dic_att[key]=value
                    if not dic_att.has_key('燃油标号'):
                        continue
                    dic_che[chekuan] = dic_att

    #                if dic_att['工信部']=='-':
    #                    continue
                    #if float(dic_att['燃油标号'])>=max:
                    #    max = float(dic_att['燃油标号'])
                    #    dic_tmp = dic_att
                else:
                    continue
            except Exception as e:
                continue
    print len(dic_che),json.dumps(dic_che['轻客/南京依维柯/依维柯得意/2014款 2.8T-V35 NJ5044XXYQZA43S4'], encoding="UTF-8", ensure_ascii=False)
    step1(dic_che)
  #  step2(dic_che)










