# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeployLog',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('log', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeploySetting',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('branch', models.CharField(max_length=191)),
                ('command', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HookLog',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('data', jsonfield.fields.JSONField()),
                ('created_at', models.DateTimeField(verbose_name='レコード作成日時', auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('hub', models.CharField(max_length=191, db_index=True)),
                ('user', models.CharField(max_length=191)),
                ('name', models.CharField(max_length=191)),
                ('full_name', models.CharField(max_length=191, db_index=True)),
                ('secret', models.CharField(max_length=191, db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='deploysetting',
            name='repository',
            field=models.ForeignKey(to='core.Repository'),
            preserve_default=True,
        ),
    ]
