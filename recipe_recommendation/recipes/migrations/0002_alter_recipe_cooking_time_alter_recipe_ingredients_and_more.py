# Generated by Django 5.1.6 on 2025-02-26 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.TextField(db_index=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='recipe_type',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='title',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]
