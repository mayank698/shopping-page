# Generated by Django 3.1.7 on 2021-03-28 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20210328_1210'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='phone_no',
            new_name='phone',
        ),
    ]
