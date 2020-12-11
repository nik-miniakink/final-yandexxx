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
        return f'{self.name}({self.units_of_measurement})'

class Tags(models.Model):
    name = models.CharField(max_length=10, null=False, default='')
    slug = models.SlugField(max_length=15, unique=True, default='', null=False)
    style = models.CharField(max_length=15, default='purple')

    def __str__(self):
        return self.name


class Recipes(models.Model):
    """
    Info about recipe
    """
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='irecipes/%d_%m_%Y/')
    description = models.CharField(max_length=1000)
    ingredient_in = models.ManyToManyField('IngredientIncomposition',blank=False)
    tags = models.ManyToManyField('Tags')
    pub_date = models.DateTimeField(auto_now_add=True)
    time = models.PositiveSmallIntegerField(default=10)
    # slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class IngredientIncomposition(models.Model):
    """
    Info about composition in recipe
    """
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient,on_delete=models.DO_NOTHING)
    quantity = models.SmallIntegerField()

    def __str__(self):
        return self.ingredient.name



class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follower", verbose_name="Подписчик")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="following", verbose_name="Автор постов")


class Favorites(models.Model):
    fuser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorites_user", verbose_name="Пользователь")
    recipe = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, related_name="favorite_recipe", verbose_name="Рецепт в избранном")


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shoplist_user", verbose_name="Пользователь")
    recipe = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, related_name="shoplist_recipe", verbose_name="Рецепт с продуктами для покупки")