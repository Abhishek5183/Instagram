# Generated by Django 4.2.1 on 2023-08-25 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_userprofile_bio_alter_userprofile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.CharField(default='I am no one to harm you. I’ll let karma bash you.', max_length=100),
        ),
    ]