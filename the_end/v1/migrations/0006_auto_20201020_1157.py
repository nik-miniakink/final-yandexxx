# Generated by Django 3.1.2 on 2020-10-20 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('v1', '0005_auto_20201020_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.DO_NOTHING, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(default=123, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='units_of_measurement',
            field=models.CharField(choices=[('шт', 'шт'), ('г', 'г'), ('ст.л', 'ст.л'), ('ч.л', 'ч.л'), ('мл', 'мл')], max_length=20),
        ),
    ]