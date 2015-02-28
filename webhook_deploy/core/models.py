from django.db import models
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


class DeploySetting(models.Model):
    repository = models.ForeignKey(Repository)
    branch = models.CharField(max_length=191)
    command = models.TextField()


class HookLog(models.Model):
    body = JSONField()


class DeployLog(models.Model):
    log = models.TextField()
