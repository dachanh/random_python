import os
import redis  
import yaml
from flask.cli import FlaskGroup
from rq import Worker , Queue , Connection 

with open('./config.yaml','r') as f:
    config = yaml.load(f,Loader=yaml.SafeLoader)

@cli.command("run_worker")
def run_worker():
    redis_connection = redis.from_url(config['REDIS_URL'])
    with Connection(redis_connection):
        worker = Worker(config['QUEUES'])
        worker.work()

if __name__ == "__main__":
    cli()