from django.contrib import admin
from django.urls import path,  include
from . import views


urlpatterns = [
    # path("recipe/new/", views.user_recipe_new, name="recipe_new"),

    path("follow/", views.follow_index, name="follow_index"),
    path("author/<int:user_id>/",views.author_list, name="author"),
    path("author/<int:user_id>/follow/", views.profile_follow, name="follow"),
    path("author/<int:user_id>/unfollow/", views.profile_unfollow, name="unfollow"),
    path("recipe/<int:recipe_id>/", views.recipe_view, name="recipe_view"),
    path("recipe/new/", views.recipe_create, name="recipe_new"),
    path("", views.index, name="index"),

]
