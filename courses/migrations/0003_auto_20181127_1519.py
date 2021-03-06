# Generated by Django 2.1.3 on 2018-11-27 18:19

import courses.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20181127_1508'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='module',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='content',
            name='order',
            field=courses.fields.OrderField(blank=True, default=0, verbose_name='Orden'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='module',
            name='order',
            field=courses.fields.OrderField(blank=True, default=0, verbose_name='Orden'),
            preserve_default=False,
        ),
    ]
