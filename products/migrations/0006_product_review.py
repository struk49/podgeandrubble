# Generated by Django 3.2.25 on 2024-03-23 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='review',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]