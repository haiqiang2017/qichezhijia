#coding:utf-8
import csv

def savecsv():

	all = {}

	f = open("attribute.txt",'rb')

	for i in f.readlines():
		try:
			line = i.strip().split(",")
			fid = line[0]
			name = fid.split("/",1)[1]
			type = fid.split("/",1)[0]
			all[name] = {}
			all[name]["车类型"] =type
			for j in line:
				if ":" in j:
					line2 = j.split(":")
					k = line2[0]
					v = line2[1]
					all[name][k] = v
		except Exception as e:
			print str(e),i
			continue

	out = open('carhome_info.csv','a')
	csv_write = csv.writer(out,dialect='excel')
	max_num = 0
	for i in all:
		num = len(all[i])
		if num > max_num:
			max_num = num
		else:
			continue
	print max_num
	for i in all:
		line = ["name"]
		if len(all[i]) == max_num:
			for j in all[i]:
				line.append(j)
			csv_write.writerow(line)
			break
	for i in all:
		data = [i]
		for k in line[1:]:
			if k in all[i]:
				#print all[i][k]
				data.append(all[i][k])
			else:
				data.append("NULL")
		csv_write.writerow(data)

	print "write over"

if __name__ == '__main__':
	savecsv()


