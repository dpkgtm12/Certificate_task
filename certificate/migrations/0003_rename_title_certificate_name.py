# Generated by Django 4.0.4 on 2023-07-19 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0002_certificate_pdf'),
    ]

    operations = [
        migrations.RenameField(
            model_name='certificate',
            old_name='title',
            new_name='name',
        ),
    ]
