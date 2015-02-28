from django.contrib import admin

from core import models


admin.site.register(models.Repository)
admin.site.register(models.DeploySetting)

admin.site.register(models.HookLog)
admin.site.register(models.DeployLog)
