# Generated by Django 2.1.5 on 2019-02-06 15:59

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
            preserve_default=False,
        ),
    ]
