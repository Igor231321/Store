# Generated by Django 5.1.8 on 2025-05-15 05:23

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariation',
            name='color',
        ),
        migrations.AlterModelOptions(
            name='attribute',
            options={'verbose_name': 'Атрибут', 'verbose_name_plural': 'Атрибути'},
        ),
        migrations.AlterModelOptions(
            name='brand',
            options={'verbose_name': 'Бренд', 'verbose_name_plural': 'Бренди'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категорія', 'verbose_name_plural': 'Категорії'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Товар', 'verbose_name_plural': 'Товари'},
        ),
        migrations.AlterModelOptions(
            name='productvariation',
            options={'ordering': ['price'], 'verbose_name': 'Варіації товару', 'verbose_name_plural': 'Варіації товару'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='image',
        ),
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='category',
            name='title',
        ),
        migrations.RemoveField(
            model_name='product',
            name='characteristics',
        ),
        migrations.RemoveField(
            model_name='product',
            name='title',
        ),
        migrations.RemoveField(
            model_name='productvariation',
            name='attribute',
        ),
        migrations.AddField(
            model_name='attribute',
            name='slug',
            field=models.SlugField(max_length=155, null=True, unique=True, verbose_name='SLUG_URL'),
        ),
        migrations.AddField(
            model_name='brand',
            name='slug',
            field=models.SlugField(max_length=155, null=True, unique=True, verbose_name='SLUG_URL'),
        ),
        migrations.AddField(
            model_name='category',
            name='level',
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='lft',
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(default=0, max_length=50, unique=True, verbose_name='Назва'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='product.category', verbose_name='Батьківська категорія'),
        ),
        migrations.AddField(
            model_name='category',
            name='rght',
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(default=0, max_length=155, unique=True, verbose_name='Название'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attribute',
            name='name',
            field=models.CharField(max_length=155, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=155, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='product.brand'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.category', verbose_name='Категорія'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='Опис'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=155, null=True, unique=True, verbose_name='SLUG_URL'),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='article',
            field=models.CharField(max_length=255, verbose_name='Артикул'),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/', verbose_name='Зображення'),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ціна'),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='Кількість товару'),
        ),
        migrations.AlterModelTable(
            name='category',
            table=None,
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=50, verbose_name='Значення')),
                ('attribute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.attribute', verbose_name='Атрибут')),
            ],
            options={
                'verbose_name': 'Значення атрибута',
                'verbose_name_plural': 'Значення атрибутів',
                'db_table': 'attribute_value',
            },
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='attribute_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.attributevalue', verbose_name='Атрибут'),
        ),
        migrations.CreateModel(
            name='ProductCharacteristics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(max_length=155, null=True, unique=True, verbose_name='SLUG_URL')),
                ('value', models.CharField(max_length=50, verbose_name='Значення')),
                ('product_variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristics', to='product.productvariation')),
            ],
            options={
                'verbose_name': 'Характеристика',
                'verbose_name_plural': 'Характеристики',
                'db_table': 'product_characteristics',
            },
        ),
        migrations.DeleteModel(
            name='Color',
        ),
    ]
