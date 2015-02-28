import json
import io
import subprocess
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
    # X-Hub-Signature
    # signature = request.META.get('HTTP_X_HUB_SIGNATURE')
    # X-Github-Delivery
    # delivery = request.META.get('HTTP_X_GITHUB_DELIVERY')

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
    branch = payload.get('ref').replace('refs/heads/', '')

    deploy_settings = repo.deploysetting_set.filter(branch=branch)
    if not deploy_settings:
        return {'error': 'no deploy settings'}

    ret = []
    for deploy in deploy_settings:
        try:
            log = subprocess.check_output(['ls', '-l'])
            command = 'ls -l'
            models.DeployLog.objects.create(log=log, return_code=0)
            ret.append({'command': command, 'log': log.decode('utf-8')})
        except subprocess.CalledProcessError as e:
            print(e)
    return {'data': ret}


def github_release(request, payload):
    if payload.get('prerelease'):
        pass
