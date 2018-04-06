# Generated by Django 2.0.4 on 2018-04-06 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_user_img_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='img_profile_thumbnail',
            field=models.ImageField(blank=True, upload_to='user'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]