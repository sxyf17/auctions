# Generated by Django 4.2.5 on 2023-10-19 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_listing_imageurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='comment',
            field=models.TextField(max_length=5000, null=True),
        ),
    ]
