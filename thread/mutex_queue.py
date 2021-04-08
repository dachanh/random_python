import queue 
import time
import json
import os
import threading 
import requests
import argparse 
my_parser = argparse.ArgumentParser(description='List the content of a folder')

my_parser.add_argument('--img_dir',
                       metavar='img_dir',
                       type=str,
                       help='the path to list')

args = my_parser.parse_args()
folder = args.img_dir
queue = queue.Queue()

def is_img(img):
    return not os.path.splitext(img)[1] in ['.ini','.zip','.ZIP','.json','.docx','.rar'] 

class ThreadRequest(threading.Thread):
    def __init__(self,queue,host):
        threading.Thread.__init__(self)
        self.queue = queue
        self.host = host
    
    def run(self):
        while True:
            namefile = self.queue.get()
            files = {'file':open(namefile,'rb')}
            try:
                data = requests.post(self.host,files=files)
                basename = os.path.splitext(os.path.basename(namefile))[0]
                json_file = os.path.join(os.path.dirname(namefile),basename+'.json')
                with open(json_file,'w',encoding='utf8') as f:
                    json.dump(data.json(),f,ensure_ascii=False,indent=5)
            except Exception as e:
                print(namefile,e)
            self.queue.task_done()

img_list = []
host = 'http://172.16.5.100:8081/cv/api/v1/ocr/idcard'
for r,d,f in os.walk(folder):
    for file in f:
        img_list.append(os.path.join(r,file))
img_list = list(filter(is_img,img_list))
start = time.time()
print(len(img_list))
for i in range(3):
    t = ThreadRequest(queue,host)
    t.setDaemon(True)
    t.start()

for index , file in enumerate(img_list):
    print(index,file)
    queue.put(file)
try:
    queue.join()
except Exception as e :
    print(e)
    
print(time.time()-start)
