import json
import shlex
import subprocess
import threading
# import time
import pytz
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from core import models

jst = pytz.timezone('Asia/Tokyo')


def create_request_dict(request):
    meta = {}
    # bodyはrequest.POSTより先に読み出す必要がある
    body = request.body.decode('utf-8')

    for k, v in request.META.items():
        if k.startswith(('HTTP_', 'REMOTE_')):
            meta[k.lower()] = v

    res = {
        'datetime': datetime.now(jst).isoformat(),
        'get': dict(request.GET),
        'post': dict(request.POST),
        'body': body,
        'cookies': dict(request.COOKIES),
        'path': request.path,
        'meta': meta,
        'encoding': request.encoding,
        'method': request.method,
    }

    # POST bodyがjsonであればシリアライズ結果も返す
    try:
        body_json = json.loads(body)
        res['body_json'] = body_json
    except:
        pass

    return res


@csrf_exempt
def webhook_github(request):
    models.HookLog.objects.create(data=create_request_dict(request))

    # X-Github-Event
    event = request.META.get('HTTP_X_GITHUB_EVENT')
    body = request.body.decode('utf-8')

    try:
        body_json = json.loads(body)
    except:
        return JsonResponse({'error': 'cannot decode body like json'})

    if event == 'push' or True:
        ret = github_push(request, body_json)

    if event == 'release':
        github_release(request, body_json)

    if event == 'deployment_status':
        pass

    return JsonResponse(ret)


def github_push(request, payload):
    try:
        repo_fullname = payload['repository']['full_name']
    except:
        return {'error': 'payload repo_fullname'}
    try:
        repo = models.Repository.objects.get(hub='github', full_name=repo_fullname)
    except models.Repository.DoesNotExist:
        return {'error': 'repository not exist'}

    # X-Hub-Signature
    signature = request.META.get('HTTP_X_HUB_SIGNATURE')
    if not repo.secret == signature:
        return {'error': 'incorrect signature'}

    # X-Github-Delivery
    # delivery = request.META.get('HTTP_X_GITHUB_DELIVERY')

    branch = payload.get('ref').replace('refs/heads/', '')

    deploy_settings = repo.deploysetting_set.filter(branch=branch)
    if not deploy_settings:
        return {'error': 'no deploy settings'}

    for deploy in deploy_settings:
        exec_command(deploy)
    return {'data': ''}


def update_log(p1):
    output, err = p1.communicate()
    models.DeployLog.objects.create(log=output, return_code=p1.returncode)
    # ret.append({'command': command, 'log': log.decode('utf-8')})


def exec_command(deploy):
    cmd = ['ansible-playbook']
    cmd.extend(shlex.split(deploy.command))
    p1 = subprocess.Popen(cmd)
    t = threading.Thread(target=update_log, args=(p1,))
    # t.setDaemon(True)
    t.start()
    # t.join()


def github_release(request, payload):
    if payload.get('prerelease'):
        pass
