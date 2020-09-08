from flask import Blueprint, render_template, Response, request
from server_flask import tasks 
from server_flask.extensions import celery 

testapi = Blueprint('__testapi__',__name__)


@testapi.route('/',methods=['GET'])
def index()->Response:
    resq = None 
    if request.method == 'GET':
        a = int(request.args.get('a')) if 'a' in request.args else 1
        b =  int(request.args.get('b')) if 'b' in request.args else 1
        resq = tasks.add.delay(a,b)
    if not resq is None  : 
        return str(resq.status) + ' ' + resq.task_id
    return "ERROR"
@testapi.route('/result/<task_id>')
def result(task_id):
    res = celery.AsyncResult(task_id)
    return  str(res.result)
    