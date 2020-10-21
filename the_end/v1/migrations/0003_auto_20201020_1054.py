# Generated by Django 3.1.2 on 2020-10-20 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0002_auto_20201020_1052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredientincomposition',
            name='ingredient',
        ),
        migrations.AddField(
            model_name='ingredientincomposition',
            name='ingredient',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.DO_NOTHING, to='v1.ingredient'),
            preserve_default=False,
        ),
    ]
