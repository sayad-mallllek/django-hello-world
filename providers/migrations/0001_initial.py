# Generated by Django 4.2.13 on 2024-05-18 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DeliveryProvider',
            fields=[
                ('baseprovider_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='providers.baseprovider')),
            ],
            options={
                'abstract': False,
            },
            bases=('providers.baseprovider',),
        ),
        migrations.CreateModel(
            name='ShippingProvider',
            fields=[
                ('baseprovider_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='providers.baseprovider')),
                ('price_per_kg', models.FloatField()),
                ('address', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('providers.baseprovider',),
        ),
    ]
