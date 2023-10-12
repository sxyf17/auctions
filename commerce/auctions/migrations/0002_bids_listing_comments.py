# Generated by Django 4.2.5 on 2023-10-06 23:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_amount', models.PositiveIntegerField()),
                ('highestBid', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=1024)),
                ('buyPrice', models.PositiveIntegerField()),
                ('bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listingBids', to='auctions.bids')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listingOwner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=256)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userComment', to=settings.AUTH_USER_MODEL)),
                ('listingComment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listingComment', to='auctions.listing')),
            ],
        ),
    ]