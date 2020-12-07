from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.dates import YearArchiveView, DayArchiveView
from django.utils.crypto import get_random_string
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext as _

from .models import Building
#from .forms import ( ProjectStationCreateForm, StationImageCreateForm,
    #ProjectMapDxfCreateForm)

class BuildingListView(PermissionRequiredMixin, ListView):
    model = Building
    permission_required = 'bimblog.view_building'
    context_object_name = 'builds'
    paginate_by = 12
