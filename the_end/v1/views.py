from .models import Recipe, User, Ingredient, IngredientIncomposition, Tags, Follow
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .form import  RecipeCreateForm
from django.contrib.auth.decorators import login_required


def you_shall_not_pass(func):
    """
    Проверяет является ли юзер обратится к своему профилю
    :param func:
    :return:
    """
    def wrapper(request, *args, **kwargs):
        user_profile = get_object_or_404(User, username=kwargs['username'])
        if request.user == user_profile:
            return redirect('index')
        return func(request, *args, **kwargs)
    return wrapper

# done
def index(request):
    """
    Отрисовывает главную страницу и показывает по 6 постов на странице
    :param request:
    :return:
    """
    recipe_list = Recipe.objects.order_by("-pub_date").all()
    # count = post_list.count

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'indexAuth.html', {
        'page': page,
        'paginator': paginator,
        'posts': recipe_list,
        'page_number': page_number
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
    recipe = get_object_or_404(Recipe, id=recipe_id)

    return render(request, 'singlePage.html', {
        'recipe' : recipe
    })



# done
def author_list(request, user_id):
    user = get_object_or_404(User,id=user_id)
    recipe_list = Recipe.objects.filter(author=user)

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'authorRecipe.html',{
        'page': page,
        'paginator': paginator,
        'posts': recipe_list,
        'page_number': page_number
    })




@login_required
def follow_index(request):

    """
    Показывает список рецептов полписанных авторов
    :param request:
    :return:
    """
    follow = Follow.objects.filter(user=request.user).all()
    authors = (item.author.id for item in follow)
    recipe_list = Recipe.objects.filter(author__in=authors).order_by("-pub_date").all()

    paginator = Paginator(recipe_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'myFollow.html', {
        'page': page,
        'paginator': paginator,
        'recipe': recipe_list,
    })



@you_shall_not_pass
@login_required
def profile_follow(request, username):

    author = User.objects.get(username=username)
    follow = Follow.objects.filter(author=author) or None
    if follow is None:
        Follow.objects.create(user=request.user, author=author)

    return redirect('profile', username)


@you_shall_not_pass
@login_required
def profile_unfollow(request, username):
    author = User.objects.get(username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('profile', username)





# @login_required
# def user_recipe_new(request):
#     head_form = 'Создание рецепта'
#     text_btn_form = 'Создать рецепт'
#     form = RecipeCreateForm(
#         request.POST or None,
#         files=request.FILES or None
#     )
#
#     if request.method == "POST" and form.is_valid():
#         newRecipe = form.save(commit=False)
#         newRecipe.author = request.user
#         newRecipe.save()
#
#         ingredient_temp = []
#         for fing in request.POST:
#             t = fing.split('_')
#             if 'nameIngredient' == t[0]:
#                 ingredient_temp.append(request.POST[f'nameIngredient_{t[1]}'])
#
#                 if request.POST[f'valueIngredient_{t[1]}'] == '':
#                     quantity = 0
#                 else:
#                     quantity = int(request.POST[f'valueIngredient_{t[1]}'])
#                 ingredient = Ingredient.objects.get(
#                     title=request.POST[f'nameIngredient_{t[1]}'])
#                 ingredients_add = IngredientIncomposition.objects.create(
#                     recipe=newRecipe,
#                     quantity=quantity
#                 )
#                 ingredients_add.save()
#         form.save_m2m()
#         return redirect(
#             'view_recipe',
#             user_id=request.user.id,
#             id=newRecipe.id
#         )
#
#
#     tags = Tags.objects.all()
#     return render(request, "formRecipe.html", {
#         'form': form,
#         'head_form': head_form,
#         'tags': tags,
#         'text_btn_form': text_btn_form
#     })