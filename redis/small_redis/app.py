import flask  
import time
from rq import Queue 
from rq.job import Job
from instance_worker import conn_redis
from flask import Flask , request 

app = Flask(__name__)
q =  Queue(connection=conn_redis)

def background_job(n):
    delay = 2 
    print("task running")
    time.delay(delay)

    print(len(n))
    return len(n)


@app.route('/task',methods=['GET'])
def make_tasking():
    if request.method == "GET":
        text = request.args.get('text') if 'text' in request.args else ""
        job =  q.enqueue_call(background_job, [text])
        return f"Task ({job.id}) added to queue at {job.enqueued_at}"
    return "invalid request"
if __name__ == "__main__":
    app.run()