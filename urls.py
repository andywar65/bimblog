from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (BuildingListView, )

app_name = 'bimblog'
urlpatterns = [
    path('', BuildingListView.as_view(), name = 'building_list'),
    ]
