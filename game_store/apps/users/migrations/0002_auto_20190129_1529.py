# Generated by Django 2.1.5 on 2019-01-29 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[(0, 'Player'), (1, 'Developer')], max_length=1),
        ),
    ]
