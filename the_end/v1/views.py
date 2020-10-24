from .models import Recipe
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

def index(request):
    """
    Отрисовывает главную страницу и показывает по 5 постов на странице
    :param request:
    :return:
    """
    post_list = Recipe.objects.all()
    # count = post_list.count

    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'index.html', {
        'page': page,
        'paginator': paginator,
        'posts': post_list,
        'page_number': page_number
    })