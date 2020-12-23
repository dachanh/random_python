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
                print(e)
            self.queue.task_done()

img_list = []
host = 'http://ocr.dtroute.com/idcard?debug=True'
for r,d,f in os.walk(folder):
    for file in f:
        img_list.append(os.path.join(r,file))
start = time.time()
for i in range(5):
    t = ThreadRequest(queue,host)
    t.setDaemon(True)
    t.start()

for file in img_list:
    queue.put(file)

queue.join()
print(time.time()-start)
