# Generated by Django 5.1.1 on 2024-10-13 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_address_user_address_proof_document_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_naame',
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]