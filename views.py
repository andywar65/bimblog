from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
    FormView,)
from django.views.generic.dates import YearArchiveView, DayArchiveView
from django.utils.crypto import get_random_string
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext as _

from .models import Building
from .forms import ( BuildingCreateForm, BuildingUpdateForm, BuildingDeleteForm,)

class BuildingListView(PermissionRequiredMixin, ListView):
    model = Building
    permission_required = 'bimblog.view_building'
    context_object_name = 'builds'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'created' in self.request.GET:
            context['created'] = self.request.GET['created']
        elif 'modified' in self.request.GET:
            context['modified'] = self.request.GET['modified']
        elif 'deleted' in self.request.GET:
            context['deleted'] = self.request.GET['deleted']
        return context

class BuildingDetailView(PermissionRequiredMixin, DetailView):
    model = Building
    permission_required = 'bimblog.view_building'
    context_object_name = 'build'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #we add the following to feed the map
        context['mapbox_token'] = settings.MAPBOX_TOKEN
        return context

class BuildingCreateView( PermissionRequiredMixin, CreateView ):
    model = Building
    permission_required = 'bimblog.add_building'
    form_class = BuildingCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'created' in self.request.GET:
            context['created'] = self.request.GET['created']
        elif 'modified' in self.request.GET:
            context['modified'] = self.request.GET['modified']
        elif 'deleted' in self.request.GET:
            context['deleted'] = self.request.GET['deleted']
        #we add the following to feed the map
        context['mapbox_token'] = settings.MAPBOX_TOKEN
        return context

    def get_success_url(self):
        if 'add_another' in self.request.POST:
            return (reverse('bimblog:building_create') +
                f'?created={self.object.title}')
        else:
            return (reverse('bimblog:building_list') +
                f'?created={self.object.title}')

class BuildingUpdateView(PermissionRequiredMixin, UpdateView):
    model = Building
    permission_required = 'bimblog.change_building'
    form_class = BuildingUpdateForm
    template_name = 'bimblog/building_update_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #we add the following to feed the map
        context['mapbox_token'] = settings.MAPBOX_TOKEN
        return context

    def get_success_url(self):
        if 'add_another' in self.request.POST:
            return (reverse('bimblog:building_create') +
                f'?modified={self.object.title}')
        else:
            return (reverse('bimblog:building_list') +
                f'?modified={self.object.title}')

class BuildingDeleteView(PermissionRequiredMixin, FormView):
    model = Building
    permission_required = 'bimblog.delete_building'
    form_class = BuildingDeleteForm
    template_name = 'bimblog/building_delete_form.html'

    def setup(self, request, *args, **kwargs):
        super(BuildingDeleteView, self).setup(request, *args, **kwargs)
        self.build = get_object_or_404( Building, slug = self.kwargs['slug'] )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.build.title
        return context

    def form_valid(self, form):
        self.build.delete()
        return super(BuildingDeleteView, self).form_valid(form)

    def get_success_url(self):
        return reverse('bimblog:building_list') + f'?deleted={self.build.title}'
