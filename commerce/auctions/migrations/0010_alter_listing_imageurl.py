# Generated by Django 4.2.5 on 2023-10-18 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_category_listing_alter_watchlist_listings_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='imageUrl',
            field=models.URLField(max_length=1024, null=True),
        ),
    ]
