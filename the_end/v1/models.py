from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ingredient(models.Model):
    """
    Info about ingredient
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    measurement = (
        ('шт', 'шт'),
        ('г', 'г'),
        ('ст.л', 'ст.л'),
        ('ч.л', 'ч.л'),
        ('мл','мл')
    )

    units_of_measurement = models.CharField(choices=measurement, max_length=20)

    def __str__(self):
        return self.name



class Recipe(models.Model):
    """
    Info about recipe
    """
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200)
    # image =
    description = models.CharField(max_length=1000)
    ingredient_in = models.ManyToManyField('IngredientIncomposition')

    tag=(
        ('завтрак','завтрак'),
        ('обед','обед'),
        ('ужин','ужин'),
    )  ## Заменить на выбор из многих

    time = models.IntegerField(default=10)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class IngredientIncomposition(models.Model):
    """
    Info about composition in recipe
    """
    ingredient = models.ForeignKey(Ingredient,on_delete=models.DO_NOTHING)
    quantity = models.CharField(max_length=10)

    def __str__(self):
        return self.ingredient.name






