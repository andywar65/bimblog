from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (BuildingListView, BuildingDetailView, BuildingCreateView,
    BuildingUpdateView, BuildingDeleteView)

app_name = 'bimblog'
urlpatterns = [
    path('', BuildingListView.as_view(), name = 'building_list'),
    path('add/', BuildingCreateView.as_view(), name = 'building_create'),
    path('<slug>/', BuildingDetailView.as_view(), name = 'building_detail'),
    path('<slug>/change/', BuildingUpdateView.as_view(), name = 'building_change'),
    path('<slug>/delete/', BuildingDeleteView.as_view(), name = 'building_delete'),
    ]
