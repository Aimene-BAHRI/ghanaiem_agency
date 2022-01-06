# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from main.views import annonce_detail

app_name = 'home' 
urlpatterns = [

    # The home page
    path('', views.index, name='index'),
    path('info', views.info, name='info'),

    path('rubriques/creer', views.create_rubrique, name='create_rubrique'),
    path('rubriques', views.rubriques, name='rubriques'),
    path('rubriques/<pk>', views.rubrique, name='rubrique'),
    path('rubriques/<pk>/modifier', views.edit_rubrique, name='edit_rubrique'),
    path('rubriques/<pk>/supprimer', views.delete_rubrique, name='delete_rubrique'),

    path('annonces', views.annonces, name='annonces'),
    path('annonces/creer', views.create_annonce, name='create_annonce'),
    path('annonces/<pk>', views.annonce, name='annonce'),
    path('annonces/<pk>/detail', annonce_detail, name='annonce_detail'),
    path('annonces/<pk>/modifier', views.edit_annonce, name='edit_annonce'),
    path('annonces/<pk>/supprimer', views.delete_annonce, name='delete_annonce'),

    path('endroits', views.endroits, name='endroits'),
    path('endroits/creer', views.create_endroit, name='create_endroit'),
    path('endroits/<pk>', views.endroit, name='endroit'),
    path('endroits/<pk>/modifier', views.edit_endroit, name='edit_endroit'),
    path('endroits/<pk>/supprimer', views.delete_endroit, name='delete_endroit'),

    path('reservations', views.reservations, name="reservations"),
    path('reservations/<pk>/supprimer', views.delete_reservation, name='delete_reservation'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
