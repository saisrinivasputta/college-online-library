# Generated by Django 2.2.8 on 2020-12-23 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0002_auto_20201223_1822'),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateTimeField(blank=True, null=True)),
                ('return_date', models.DateTimeField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Library.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_no', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=10)),
                ('branch', models.CharField(max_length=3)),
                ('total_books_due', models.CharField(default=0, max_length=10)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('pic', models.ImageField(blank=True, upload_to='profile_image')),
            ],
        ),
        migrations.DeleteModel(
            name='StudentExtra',
        ),
        migrations.AddField(
            model_name='borrower',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Library.Student'),
        ),
    ]
