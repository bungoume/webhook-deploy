from django.db import models
from django.utils import timezone
from jsonfield import JSONField


class Repository(models.Model):
    # github, gitbucket, etc...
    hub = models.CharField(max_length=191, db_index=True)
    # user
    user = models.CharField(max_length=191)
    # repository_name
    name = models.CharField(max_length=191)
    # username/reponame
    full_name = models.CharField(max_length=191, db_index=True)
    # Secret Key
    secret = models.CharField(max_length=191, db_index=True)

    def __str__(self):
        return '{}: {}'.format(self.hub, self.full_name)


class DeploySetting(models.Model):
    repository = models.ForeignKey(Repository)
    branch = models.CharField(max_length=191)
    command = models.TextField()

    def __str__(self):
        return '{}: {}'.format(self.repository, self.branch)


class HookLog(models.Model):
    data = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        dt_text = timezone.localtime(self.created_at).strftime('%Y-%m-%d %H:%M:%S')
        return '{}: {}'.format(dt_text, self.data.get('path'))


class DeployLog(models.Model):
    log = models.TextField()
    return_code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        dt_text = timezone.localtime(self.created_at).strftime('%Y-%m-%d %H:%M:%S')
        return '{}: {}'.format(dt_text, self.return_code)
