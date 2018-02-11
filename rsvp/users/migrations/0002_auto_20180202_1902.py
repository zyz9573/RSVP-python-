# Generated by Django 2.0.2 on 2018-02-02 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='realuser',
            name='guest_event',
            field=models.ManyToManyField(related_name='guest_event', to='event.Event'),
        ),
        migrations.AddField(
            model_name='realuser',
            name='owner_event',
            field=models.ManyToManyField(related_name='owner_event', to='event.Event'),
        ),
        migrations.AddField(
            model_name='realuser',
            name='vendor_event',
            field=models.ManyToManyField(related_name='vendor_event', to='event.Event'),
        ),
    ]