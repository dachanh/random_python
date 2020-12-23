import queue 
import time
import json
import os
import threading 
import requests
import argparse 
"""
safe thread
"""
my_parser = argparse.ArgumentParser(description='List the content of a folder')

my_parser.add_argument('--img_dir',
                       metavar='img_dir',
                       type=str,
                       help='the path to list')

args = my_parser.parse_args()
folder = args.img_dir
in_queue = queue.Queue()
out_queue = queue.Queue()
img_list = []
host = 'http://ocr.dtroute.com/idcard?debug=True'

class ThreadRequest(threading.Thread):
    def __init__(self,in_queue,out_queue,host):
        threading.Thread.__init__(self)
        self.in_queue = in_queue 
        self.out_queue = out_queue
        self.host = host
    
    def run(self):
        while True:
            namefile = self.in_queue.get()
            try:
                files = {'file':open(namefile,'rb')}
                data = requests.post(self.host,files=files)
                self.out_queue.put((namefile,data))
            except Exception as e :
                print(namefile,e)
            self.in_queue.task_done()

class ThreadWrite(threading.Thread):
    def __init__(self,out_queue):
        threading.Thread.__init__(self)
        self.out_queue = out_queue
        
    def run(self):
        while True:
            namefile,data = self.out_queue.get()
            basename = os.path.splitext(os.path.basename(namefile))[0]
            try:
                json_file = os.path.join(os.path.dirname(namefile),basename+'.json')
                with open(json_file,'w',encoding='utf8') as f:
                    json.dump(data.json(),f,ensure_ascii=False,indent=5)
            except Exception as e :
                print(namefile,e)
            self.out_queue.task_done()


for i in range(10):
    t = ThreadRequest(in_queue,out_queue,host)
    t.setDaemon(True)
    t.start()

start = time.time()
for r,d,f in os.walk(folder):
    for file in f:
        img_list.append(os.path.join(r,file))
for it in img_list:
    in_queue.put(it)


for it in range(10):
    out_t = ThreadWrite(out_queue)
    out_t.setDaemon(True)
    out_t.start()

in_queue.join()
out_queue.join()
print(time.time() - start)