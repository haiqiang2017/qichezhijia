#coding:utf-8
import csv
f1 = "carhome_info.csv"
f2 = "result-20181025.csv"
#读取爬虫信息，key:id,value:info
all = {}
csv_file = csv.reader(open(f1,'r'))
key_list = []
for line in csv_file:
	#print line[0]
	fid = line[0]
	if fid == "name":
		for i in line[1:]:
			key_list.append(i)
	else:
		all[fid] = {}
		for j in range(len(key_list)):
			all[fid][key_list[j]] = line[j+1]
#test1
#for i in all:
#	print i,all[i]
#	break
#读取2万公司列表
all2 = {}
csv_file = csv.reader(open(f2,'r'))
key_list2 = []
for line in csv_file:
	#print line[0]
	fid = line[6]
	if fid == "third_level_model":
		for i in line[1:]:
			key_list2.append(i)
	else:
		all2[fid] = {}
		for j in range(len(key_list2)):
			all2[fid][key_list2[j]] = line[j+1]
#test2
#for i in all2:
#	print i,all2[i]
#	break

#对应信息
out = open('car_result.csv','a')
csv_write = csv.writer(out,dialect='excel')
#column = key_list2
column = []
column.append("name")
column.extend(key_list)
csv_write.writerow(column)

other = []
data = []
for j in all:
	flag = "0"
	for i in all2:
		data = []
		key = i.split("-")
		#print i,j
		#break
		if key[0] in j and key[1] in j and key[2] in j:
			flag = "1"
			#continue
			#print "ok"
			#for k in column[:17]:
			#	data.append(all2[i][k])
			#data.append(j)
			#for p in column[18:]:
			#	data.append(all[j][p])
        		#csv_write.writerow(data)
		else:
			continue
	if flag == "0":
		other.append(j)
print len(other)
print len(set(other))
print len(column)
other = set(other)
for i in other:
	data = []
	data.append(i)
	for p in column[1:]:
		data.append(all[i][p])
        csv_write.writerow(data)
			
print ("write over")				

