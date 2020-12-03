from django.contrib import admin
from django.urls import path,  include
from . import views


urlpatterns = [
    path("ingredients", views.get_ingredients, name="get_ingredients"),
    path("recipe/new/", views.user_recipe_new, name="recipe_new"),

    path("follow/", views.follow_index, name="follow_index"),
    path("author/<int:user_id>/",views.author_list, name="author"),

    path("recipe/<int:recipe_id>/", views.recipe_view, name="recipe_view"),
    # path("recipe/new/", views.recipe_create, name="recipe_new"),
    path("favorite/", views.favorites, name="favorites"),
    path("favorites", views.add_favorite, name="add_favorite"),
    path("favorites/", views.add_favorite, name="add_favorite"),
    path("favorites/<int:recipe_id>",
         views.delete_favorite, name="delete_favorite"),

    path("subscriptions", views.add_subscription, name="add_subscription"),
    path("subscriptions/", views.add_subscription, name="add_subscription"),
    path("subscriptions/<int:following_id>",
         views.delete_subscription, name="delete_subscription"),

    path("purchases", views.add_purchases, name="add_purchases"),
    path("purchases/", views.add_purchases, name="add_purchases"),
    path("purchases/<int:recipe_id>",
         views.delete_purchases, name="delete_purchases"),
    path("purchases/<int:recipe_id>/",
         views.delete_purchases, name="delete_purchases"),

    path("", views.index, name="index"),
]
