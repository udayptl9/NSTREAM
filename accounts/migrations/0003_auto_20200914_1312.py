# Generated by Django 3.1.1 on 2020-09-14 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_accounts_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='image',
            field=models.ImageField(default='profiles/default.jpg', upload_to='profiles'),
        ),
    ]