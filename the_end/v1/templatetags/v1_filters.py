from django import template
from ..models import Follow, Favorites, ShoppingList
from ..models import Recipes

register = template.Library()



@register.filter(name='items_follow')
def get_filter_values(request, author_id):
    return Recipes.objects.filter(author=author_id).order_by("pub_date")[:3]


@register.filter(name='count_recipises')
def get_filter_values(request, author_id):
    count = Recipes.objects.filter(author=author_id).count()
    return (count - 3)


@register.filter(name='in_favorites')
def get_filter_values(request, recipe_id):
    is_favorite = Favorites.objects.filter(
        recipe_id=recipe_id).filter(fuser=request.user).all()
    return is_favorite.count()


@register.filter(name='is_favorites')
def get_filter_value(request, recipe_id):
    is_favorites= Favorites.objects.filter(fuser=request.user,recipe_id=recipe_id).all()
    if is_favorites:
        return True
    return False

@register.filter(name='count_shoplist')
def get_filter_values(request):
    counts_list = ShoppingList.objects.filter(user=request.user).all()
    if counts_list.count() > 0:
        return counts_list.count()
    return 0


@register.filter(name='is_shoplist')
def get_filter_values(request, recipe_id):
    is_slist = ShoppingList.objects.filter(user=request.user).filter(
        recipe_id=recipe_id).all()
    if is_slist:
        return True
    return False    
