# Generated by Django 2.2.8 on 2020-12-23 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='name',
            new_name='nameofbook',
        ),
    ]
