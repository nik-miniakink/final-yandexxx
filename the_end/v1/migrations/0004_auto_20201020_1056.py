# Generated by Django 3.1.2 on 2020-10-20 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0003_auto_20201020_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredient_in',
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredient_in',
            field=models.ManyToManyField(to='v1.IngredientIncomposition'),
        ),
    ]