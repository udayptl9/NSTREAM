# Generated by Django 3.1.1 on 2020-09-14 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profiles'),
        ),
    ]
