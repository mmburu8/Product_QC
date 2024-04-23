# Generated by Django 4.2.5 on 2024-01-06 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('total_products', models.IntegerField()),
                ('defect_products', models.IntegerField()),
                ('passed_products', models.IntegerField()),
                ('products_retained', models.IntegerField()),
                ('customer_compliants', models.IntegerField()),
            ],
        ),
    ]