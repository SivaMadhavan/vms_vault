# Generated by Django 4.0 on 2023-12-19 14:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('po_number', models.CharField(default=uuid.uuid4, max_length=255, primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField(auto_now=True, null=True)),
                ('delivery_date', models.DateTimeField(null=True)),
                ('items', models.JSONField(null=True)),
                ('quantity', models.IntegerField(null=True)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('COMPLETED', 'COMPLETED'), ('CANCELED', 'CANCELED')], max_length=10)),
                ('quality_rating', models.FloatField(null=True)),
                ('issue_date', models.DateTimeField(null=True)),
                ('acknowledgment_date', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
