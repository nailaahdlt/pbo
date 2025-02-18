# Generated by Django 5.1.5 on 2025-02-02 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='room_images/'),
        ),
        migrations.AlterField(
            model_name='room',
            name='price_per_night',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
