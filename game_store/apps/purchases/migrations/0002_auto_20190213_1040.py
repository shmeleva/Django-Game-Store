# Generated by Django 2.1.5 on 2019-02-13 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('S', 'Succeeded'), ('F', 'Failed'), ('C', 'Canceled')], default='P', max_length=1),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
