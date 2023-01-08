# Generated by Django 3.2.16 on 2023-01-05 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_courier_paypal_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('in', 'In'), ('out', 'Out')], default='in', max_length=20),
        ),
    ]