from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name='account_list'),
    path("<uuid:account_id>/", views.detail, name='account_detail'),
    path('transfer/', views.transfer_funds, name='transfer_funds'),
]