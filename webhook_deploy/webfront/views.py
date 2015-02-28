import json
import io
import subprocess
import pytz
from datetime import datetime

from django.http import JsonResponse

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
        body_json = {}

    if event == 'push':
        github_push(request, body_json)

    if event == 'release':
        github_release(request, body_json)

    if event == 'deployment_status':
        pass

    return JsonResponse({})


def github_push(request, payload):
    try:
        repo_fullname = payload['repository']['full_name']
    except:
        return
    repo = models.Repository.objects.get(hub='github', fullname=repo_fullname)
    branch = payload.get('ref').replace('refs/heads/', '')

    deploy_settings = repo.deploy_setting_set.filter(branch=branch)
    for deploy in deploy_settings:
        try:
            log = subprocess.check_output(['ls', '-l'])
            models.DeployLog.objects.create(log=log)
        except subprocess.CalledProcessError as e:
            print(e)


def github_release(request, payload):
    if payload.get('prerelease'):
        pass
