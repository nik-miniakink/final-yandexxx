from .models import Recipes, User, Ingredient, IngredientIncomposition, Tags, Follow
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .form import RecipeForm
from django.contrib.auth.decorators import login_required

import json
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Recipes, IngredientIncomposition, Ingredient
from .models import Follow, Favorites, ShoppingList



tags_list={}

# def you_shall_not_pass(func):
#     """
#     Проверяет является ли юзер обратится к своему профилю
#     :param func:
#     :return:
#     """
#     def wrapper(request, *args, **kwargs):
#         user_profile = get_object_or_404(User, username=kwargs['username'])
#         if request.user == user_profile:
#             return redirect('index')
#         return func(request, *args, **kwargs)
#     return wrapper


def index(request):
    """
    Отрисовывает главную страницу и показывает по 6 постов на странице
    При наличии выбраных тэгов производить фильтрафию рецептов


    :param request:
    :return:
    """

    tag = request.GET.get("tag_list")
    if tag is not None:
        if tag not in tags_list:
            tags_list[tag]=tag
        else:
            del tags_list[tag]

    if len(tags_list) > 0:
        recipe_list = Recipes.objects.filter(tags__slug__in=tags_list).order_by("-pub_date").all()
    else:
        recipe_list = Recipes.objects.order_by("-pub_date").all()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    tags = Tags.objects.all()
    # if request.user.:
    # print(111111111111)
    # shop_count= ShoppingList.objects.filter(user=request.user)
    # print(shop_count)
    # else:
    #     shop_count=0
    return render(request, 'indexAuth.html', {
        'page': page,
        'paginator': paginator,
        'recipes': recipe_list,
        'page_number': page_number,
        'tags': tags,
        'tags_list': tags_list,
    })

# done
def recipe_view(request, recipe_id):
    """
    Отрисовывает страницу одиночного рецепта
    :param request:
    :param recipe_id:
    :param user_id:
    :return:
    """
    recipe = get_object_or_404(Recipes, id=recipe_id)
    tags = Tags.objects.filter(recipes=recipe)
    ings = IngredientIncomposition.objects.filter(recipe=recipe)
    return render(request, 'singlePage.html', {
        'recipe' : recipe,
        'tags': tags,
        'ings' : ings,
    })

# done
def author_list(request, user_id):
    """
    Отрисовывает страницу выбранного автора
    При наличии выделения тэгов происходит фильтрация
    :param request:
    :param user_id:
    :return:
    """
    tag = request.GET.get("tag_list")
    if tag is not None:
        if tag not in tags_list:
            tags_list[tag] = tag
        else:
            del tags_list[tag]
    user = get_object_or_404(User, id=user_id)


    if len(tags_list) > 0:
        recipe_list = Recipes.objects.filter(tags__slug__in=tags_list, author=user).order_by("-pub_date").all()
    else:
        recipe_list = Recipes.objects.filter(author=user).order_by("-pub_date").all()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    tags = Tags.objects.all()

    return render(request, 'indexAuth.html', {
        'page': page,
        'paginator': paginator,
        'recipes': recipe_list,
        'page_number': page_number,
        'tags': tags,
        'tags_list': tags_list,
    })


@login_required
def follow_index(request):

    """
    Показывает список рецептов полписанных авторов
    :param request:
    :return:
    """
    myFollow = Follow.objects.filter(
        user_id=request.user.id).order_by("author").all()
    authors = User.objects.filter(following__in=myFollow)
    paginator = Paginator(myFollow, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, 'myFollow.html', {
        'page': page,
        'paginator': paginator,
        'follow': myFollow,
        'authors':authors,
    })


@login_required
def favorites(request):

    tag = request.GET.get("tag_list")
    if tag is not None:
        if tag not in tags_list:
            tags_list[tag] = tag
        else:
            del tags_list[tag]
    user = get_object_or_404(User, id=request.user.id)

    favorite_recipes = Favorites.objects.filter(fuser=user)

    recipe_list = Recipes.objects.filter(favorite_recipe__fuser__id=request.user.id).all()


    if len(tags_list) > 0:
        recipe_list = Recipes.objects.filter(tags__slug__in=tags_list, favorite_recipe__fuser__id=request.user.id).order_by("-pub_date").all()
    else:
        recipe_list = Recipes.objects.filter(favorite_recipe__fuser__id=request.user.id).order_by("-pub_date").all()

    tags = Tags.objects.all()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'recipes': recipe_list,
        'page_number': page_number,
        'tags': tags,
        'tags_list': tags_list,
    }
    return render(request, 'favorite.html', context)


@login_required
def add_favorite(request):
    """
    Добавляет рецепт в избранное
    :param request:
    :return:
    """
    if request.method == "POST":
        recipe_id = int(json.loads(request.body).get('id'))
        recipe = get_object_or_404(Recipes,id=recipe_id)
        created = Favorites.objects.get_or_create(
            fuser=request.user, recipe=recipe)

        if not created:
            return JsonResponse({'success': False})

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@login_required
def delete_favorite(request, recipe_id):
    """
    Исключает рецепт из избранного
    """
    if request.method == "DELETE":
        user = request.user
        deleted = Favorites.objects.filter(
            fuser_id=user.id, recipe_id=recipe_id).delete()
        return JsonResponse({'success': True}) if deleted else JsonResponse({'success': False})
    else:
        return JsonResponse({'success': False})


@login_required
def add_subscription(request):
    following_id = int(json.loads(request.body).get('id'))
    following = get_object_or_404(User, id=following_id)
    if request.user.id != following_id:
        created = Follow.objects.get_or_create(
            user=request.user, author=following)
    return JsonResponse({'success': True}) if created else JsonResponse({'success': False})


@login_required
def delete_subscription(request, following_id):
    deleted = Follow.objects.filter(
        user_id=request.user.id, author_id=following_id).delete()
    return JsonResponse({'success': True}) if deleted else JsonResponse({'success': False})


def add_purchases(request):
    if request.method == "POST":
        recipe_id = int(json.loads(request.body).get('id'))
        created = ShoppingList.objects.get_or_create(
            user_id=request.user.id, recipe_id=recipe_id)
        if not created:
            return JsonResponse({'success': False})

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@login_required
def delete_purchases(request, recipe_id):
    if request.method == "DELETE":
        deleted = ShoppingList.objects.filter(
            user_id=request.user.id, recipe_id=recipe_id).delete()
        return JsonResponse({'success': True}) if deleted else JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def get_ingredients(request):
    ingredients = {}
    for key, ingredient_name in request.POST.items():
        if 'nameIngredient' in key:
            _ = key.split('_')
            ingredients[ingredient_name] = int(request.POST[
                f'valueIngredient_{_[1]}']
            )
    return ingredients


def get_ingredients_js(request):
    text = request.GET.get('query')
    data = []
    ingredients = Ingredient.objects.filter(
        name__startswith=text).all()
    for ingredient in ingredients:
        data.append(
            {'title': ingredient.name, 'dimension': ingredient.units_of_measurement})

    return JsonResponse(data, safe=False)


@login_required
def user_recipe_new(request):
    user = User.objects.get(username=request.user)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None)

    if request.method == 'POST':
        ingredients = get_ingredients(request)
        if not ingredients:
            form.add_error(None, 'Добавьте ингредиенты')
        elif form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = user
            recipe.save()
            print(request.POST)
            recipe_tags_list = request.POST.getlist('tags')
            for tag_id in recipe_tags_list:
                tag = Tags.objects.get(id=tag_id)
                recipe.tags.add(tag)

            for ing_name, quantity in ingredients.items():
                ingredient = get_object_or_404(Ingredient, name=ing_name)
                IngredientIncomposition.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=quantity)
            form.save_m2m()
            return redirect('index')
    else:
        form = RecipeForm()

    tags=Tags.objects.all()
    return render(request, 'formRecipe.html', {
        'form': form,
        'tags': tags,
    })

@login_required
def user_recipe_edit(request, recipe_id):

    recipe = get_object_or_404(Recipes, id=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe_view', id=recipe_id)

    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if request.method == "POST":
        ingredients = get_ingredients(request)
        print(11111111111111111111111111111111)
        if not ingredients:
            form.add_error(None, 'Добавьте ингредиенты')
        if form.is_valid():
            form.save()
            IngredientIncomposition.objects.filter(recipes=recipe).delete()
            print(22222222222222222222222222222222)
            for ing_name, quantity in ingredients.items():
                ingredient = get_object_or_404(Ingredient, name=ing_name)
                IngredientIncomposition.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=quantity)
            # form.save_m2m()
            return redirect('recipe_view', recipe_id=recipe.id)
    else:
        form = RecipeForm()
    tags = Tags.objects.all()
    tags_list = Tags.objects.filter(recipes=recipe)

    ingredients = IngredientIncomposition.objects.filter(recipes=recipe.id)

    return render(request, 'formChangeRecipe.html', {
        'form': form,
        'recipe': recipe,
        'tags': tags,
        'ingredients': ingredients,
        'tags_list':tags_list
    })



@login_required
def shopping_list(request):
    shopping_list = ShoppingList.objects.filter(user=request.user).all()
    return render(
        request,
        'shopping-list.html',
        {'shopping_list': shopping_list}
    )