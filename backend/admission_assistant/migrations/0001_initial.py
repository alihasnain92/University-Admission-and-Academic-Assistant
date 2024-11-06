# Generated by Django 5.1.2 on 2024-10-24 13:57

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admission_code', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=20)),
                ('program', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('reviewing', 'Under Review'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('entry_test_unlocked', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='IntentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('keywords', models.TextField(help_text='Comma-separated keywords')),
            ],
            options={
                'verbose_name': 'Intent Category',
                'verbose_name_plural': 'Intent Categories',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('verified', models.BooleanField(default=False)),
                ('admission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='admission_assistant.admission')),
            ],
        ),
        migrations.CreateModel(
            name='EntryTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_date', models.DateTimeField(blank=True, null=True)),
                ('venue', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(default='scheduled', max_length=20)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('admission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='entry_test', to='admission_assistant.admission')),
            ],
        ),
        migrations.CreateModel(
            name='Guardian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('relation', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('occupation', models.CharField(max_length=100)),
                ('income', models.DecimalField(decimal_places=2, max_digits=12)),
                ('admission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guardians', to='admission_assistant.admission')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('transaction_id', models.CharField(max_length=100, unique=True)),
                ('admission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='admission_assistant.admission')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_text', models.TextField()),
                ('priority', models.IntegerField(default=1)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='admission_assistant.intentcategory')),
            ],
            options={
                'ordering': ['-priority'],
            },
        ),
    ]
