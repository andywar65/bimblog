from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (BuildingListView, BuildingDetailView, BuildingCreateView,
    BuildingUpdateView, BuildingDeleteView, BuildingPlanCreateView,
    BuildingPlanUpdateView, BuildingPlanDeleteView, PhotoStationCreateView)

app_name = 'bimblog'
urlpatterns = [
    path('', BuildingListView.as_view(), name = 'building_list'),
    path('add/', BuildingCreateView.as_view(), name = 'building_create'),
    path('<slug>/', BuildingDetailView.as_view(), name = 'building_detail'),
    path('<slug>/change/', BuildingUpdateView.as_view(), name = 'building_change'),
    path('<slug>/delete/', BuildingDeleteView.as_view(), name = 'building_delete'),
    path('<slug>/plan/add/', BuildingPlanCreateView.as_view(),
        name = 'buildingplan_create'),
    path('<slug:build_slug>/plan/<slug:plan_slug>/change/',
        BuildingPlanUpdateView.as_view(), name = 'buildingplan_change'),
    path('<slug:build_slug>/plan/<slug:plan_slug>/delete/',
        BuildingPlanDeleteView.as_view(), name = 'buildingplan_delete'),
    path('<slug>/station/add/', PhotoStationCreateView.as_view(),
        name = 'station_create'),
    ]
