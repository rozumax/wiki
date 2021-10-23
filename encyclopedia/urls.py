from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newPage", views.newPage, name="newPage"),
    path("savePage", views.savePage, name="savePage"),
    path("randomPage", views.randomPage, name="randomPage"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("wikiAlreadyExists/<str:title>", views.wikiAlreadyExists, name="wikiAlreadyExists"),
    path("editPage/<str:title>", views.editPage, name="editPage"),
    path("saveEditedPage", views.saveEditedPage, name="saveEditedPage"),
    path("search", views.search, name="search")
]
