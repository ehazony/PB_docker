# Generated by Django 3.0.8 on 2022-05-17 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopify_app', '0002_shop_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='email',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
