from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (BuildingListView, BuildingDetailView, BuildingCreateView,
    BuildingUpdateView, BuildingDeleteView, BuildingPlanCreateView,
    BuildingPlanUpdateView, BuildingPlanDeleteView, PhotoStationCreateView,
    PhotoStationDetailView, PhotoStationUpdateView, PhotoStationDeleteView,
    StationImageCreateView, StationImageUpdateView)

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
    path('<slug:build_slug>/station/<slug:stat_slug>/',
        PhotoStationDetailView.as_view(), name = 'station_detail'),
    path('<slug:build_slug>/station/<slug:stat_slug>/change/',
        PhotoStationUpdateView.as_view(), name = 'station_change'),
    path('<slug:build_slug>/station/<slug:stat_slug>/delete/',
        PhotoStationDeleteView.as_view(), name = 'station_delete'),
    path(_('<slug:build_slug>/stations/<slug:stat_slug>/image/add/'),
        StationImageCreateView.as_view(), name = 'image_add'),
    path(_('<slug:build_slug>/stations/<slug:stat_slug>/image/<pk>/change'),
        StationImageUpdateView.as_view(), name = 'image_change'),
    ]
