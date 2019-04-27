# _*_ecoding:utf-8 _*_
import sys
import os
import time
import subprocess
import threading
import urllib
import argparse
from multiprocessing import Pool
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('./lib')

def time_change(date,time1):
    str_time = ("%s %s"%(date,time1))
    timeArray = time.strptime(str_time, "%Y%m%d %H:%M:%S")
    start_time = int(time.mktime(timeArray))
    return str(start_time)
def auto_apider(cmd):
#    global num,sum1
#    with open(logfile,'a+') as load_t:
#         load_t.write("当前下载进度为...%d/%d"%(num,sum1)+'\n')
    chdir = 'cd /volume4/autolabeling/mspout-cat-1.0.2-Linux-x86_64'
    os.system(cmd)
#    subprocess.call(cmd,shell=False)
if __name__ == "__main__":
#    timefile = sys.argv[1]
#    locfile = sys.argv[2]
#    url = 'netposa://admin:admin@172.24.49.146:2000'
    start = time.time()
    num_pool = 10
    tstr_yestoday = time.strftime('%Y%m%d', time.localtime(time.time()-86400*1))
#    tstr_yestoday = '20181015'
    cmd_list=[]
    newlist = sys.argv[1]
    base_path = '/mnt/data3/reid_down/%s'%newlist
    with open('/volume4/autolabeling/mspout-cat-1.0.2-Linux-x86_64/timelist','r') as load_a:
        for line in load_a.readlines():
            starttime = time_change(tstr_yestoday,line.strip().split(',')[0])
            endtime = time_change(tstr_yestoday,line.strip().split(',')[1])
            with open('/volume4/autolabeling/mspout-cat-1.0.2-Linux-x86_64/%s'%newlist,'r') as load_b:
                for line1 in load_b.readlines():
                    #print line1.strip()
                    #loc = line1.strip().split(',')[0]
                    road = line1.strip().split(',')[0]
                    url = line1.strip().split(',')[1]
                   # road = url.split('/')[3]
                  #  print url
                #    group = url.split('/')[-2]
                    dire = url.split('/')[-1]
#                    dire = group+dire1
                    name = "%s-%s-%s.h264" %(road,dire,starttime)
                    dir = os.path.join(base_path,tstr_yestoday)
                    if not os.path.exists(dir):
                       os.makedirs(dir)
                    out_file = os.path.join(dir,name)
                    if os.path.exists(out_file):
                       continue
                    command = '/volume4/autolabeling/mspout-cat-1.0.2-Linux-x86_64/mspout-cat -i "{0}" -o {1} -num 900 -stream_type vod -start_time {2} -end_time {3}'.format(url,out_file,starttime,endtime)
                    print command
                    cmd_list.append(command)
    p = Pool(num_pool)
    sum1 = len(cmd_list)
    logfile = newlist+'.log'
    #用于判断当前爬去的视频进度
    num = 0
    try:
       for cmd in cmd_list:
           print cmd
           try:
              p.apply_async(auto_apider,(cmd,))
              num = num + 1
           except:
              continue
    except:
       print "a error occer hear"
    else:
       p.close()
    p.join()
    end = time.time()
    print "共 "+str((end-start)/3600)+" 小时"







