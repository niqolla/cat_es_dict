# Generated by Django 4.1 on 2023-11-25 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DelRoba',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(max_length=200, null=True)),
                ('img_loc', models.CharField(max_length=200, null=True)),
                ('opis', models.TextField(null=True)),
            ],
        ),
    ]