# Generated by Django 4.2.5 on 2023-10-18 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_listing_imageurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='imageUrl',
            field=models.TextField(max_length=5000, null=True),
        ),
    ]
