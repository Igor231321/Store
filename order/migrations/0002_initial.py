# Generated by Django 5.2 on 2025-06-21 18:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Користувач'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order', verbose_name='Замовлення'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product_variation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productvariation', verbose_name='Варіація товара'),
        ),
        migrations.AddField(
            model_name='warehouse',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouses', to='order.country'),
        ),
    ]
