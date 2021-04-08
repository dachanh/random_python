from datetime import timedelta
from redis import Redis


def limited_request(r:Redis,key:str,limit:int,period: timedelta):
  
  if r.setnx(key,limit):
    r.expire(key,int(period.total_second()))
  bucket_val = r.get(key)
  if bucket_val and int(bucket_val) > 0:
    r.decrby(key,1)