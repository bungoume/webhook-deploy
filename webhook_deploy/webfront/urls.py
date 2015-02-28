from django.conf.urls import url

from webfront import views

urlpatterns = [
    url(r'^webhook/github', views.webhook_github, name='webhook_github'),
]
