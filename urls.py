from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (BuildingListView, BuildingDetailView, BuildingCreateView)

app_name = 'bimblog'
urlpatterns = [
    path('', BuildingListView.as_view(), name = 'building_list'),
    path('<slug>/', BuildingDetailView.as_view(), name = 'building_detail'),
    path('add/', BuildingCreateView.as_view(), name = 'building_create'),
    ]
