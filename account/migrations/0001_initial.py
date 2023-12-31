# Generated by Django 4.2.7 on 2023-11-24 12:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bitcoin_address', models.CharField(max_length=255)),
                ('lightning_address', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('payment_status', models.CharField(choices=[('paid', 'Paid'), ('partially_paid', 'Partially Paid'), ('not_paid', 'Not Paid'), ('unconfirmed', 'Unconfirmed')], default='not_paid', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('source', models.CharField(choices=[('bitcoin', 'Bitcoin'), ('internal', 'Internal'), ('lightning', 'Lightning')], default='internal', max_length=10)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('mensagem', models.TextField(blank=True, null=True)),
                ('bitcoin_address', models.CharField(blank=True, max_length=255, null=True)),
                ('lightning_address', models.CharField(blank=True, max_length=255, null=True)),
                ('received', models.BooleanField(default=False)),
            ],
        ),
    ]
