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

from .models import Building, BuildingPlan, PhotoStation
from .forms import ( BuildingCreateForm, BuildingUpdateForm, BuildingDeleteForm,
    BuildingPlanCreateForm, BuildingPlanDeleteForm, PhotoStationCreateForm )

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
        #we add the following to feed the map
        context['city_lat'] = settings.CITY_LAT
        context['city_long'] = settings.CITY_LONG
        context['city_zoom'] = settings.CITY_ZOOM
        context['mapbox_token'] = settings.MAPBOX_TOKEN
        return context

class BuildingDetailView(PermissionRequiredMixin, DetailView):
    model = Building
    permission_required = 'bimblog.view_building'
    context_object_name = 'build'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plans'] = context['build'].building_plan
        if 'created' in self.request.GET:
            context['created'] = self.request.GET['created']
        elif 'modified' in self.request.GET:
            context['modified'] = self.request.GET['modified']
        elif 'plan_created' in self.request.GET:
            context['plan_created'] = self.request.GET['plan_created']
        elif 'plan_modified' in self.request.GET:
            context['plan_modified'] = self.request.GET['plan_modified']
        elif 'plan_deleted' in self.request.GET:
            context['plan_deleted'] = self.request.GET['plan_deleted']
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
        context['city_lat'] = settings.CITY_LAT
        context['city_long'] = settings.CITY_LONG
        context['city_zoom'] = settings.CITY_ZOOM
        context['mapbox_token'] = settings.MAPBOX_TOKEN
        return context

    def get_success_url(self):
        if 'add_another' in self.request.POST:
            return (reverse('bimblog:building_create') +
                f'?created={self.object.title}')
        else:
            return (reverse('bimblog:building_detail',
                kwargs={'slug': self.object.slug }) +
                f'?created={self.object.title}')

class BuildingUpdateView(PermissionRequiredMixin, UpdateView):
    model = Building
    permission_required = 'bimblog.change_building'
    form_class = BuildingUpdateForm
    template_name = 'bimblog/building_form_update.html'

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
            return (reverse('bimblog:building_detail',
                kwargs={'slug': self.object.slug }) +
                f'?modified={self.object.title}')

class BuildingDeleteView(PermissionRequiredMixin, FormView):
    model = Building
    permission_required = 'bimblog.delete_building'
    form_class = BuildingDeleteForm
    template_name = 'bimblog/building_form_delete.html'

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

class BuildingPlanCreateView( PermissionRequiredMixin, CreateView ):
    model = BuildingPlan
    permission_required = 'bimblog.add_buildingplan'
    form_class = BuildingPlanCreateForm

    def setup(self, request, *args, **kwargs):
        super(BuildingPlanCreateView, self).setup(request, *args, **kwargs)
        self.build = get_object_or_404( Building, slug = self.kwargs['slug'] )

    def get_initial(self):
        initial = super( BuildingPlanCreateView, self ).get_initial()
        initial['build'] = self.build.id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'plan_created' in self.request.GET:
            context['plan_created'] = self.request.GET['plan_created']
        if 'plan_modified' in self.request.GET:
            context['plan_modified'] = self.request.GET['plan_modified']
        return context

    def get_success_url(self):
        if 'add_another' in self.request.POST:
            return (reverse('bimblog:buildingplan_create',
                kwargs={'slug': self.build.slug}) +
                f'?plan_created={self.object.title}')
        else:
            return (reverse('bimblog:building_detail',
                kwargs={'slug': self.build.slug}) +
                f'?plan_created={self.object.title}')

class BuildingPlanUpdateView( PermissionRequiredMixin, UpdateView ):
    model = BuildingPlan
    permission_required = 'bimblog.change_buildingplan'
    form_class = BuildingPlanCreateForm
    template_name = 'bimblog/buildingplan_form_update.html'
    #we have two slugs, so we need to override next attribute
    slug_url_kwarg = 'plan_slug'

    def get_object(self, queryset=None):
        #elsewhere we get the parent in setup, but here we also need object
        plan = super(BuildingPlanUpdateView, self).get_object(queryset=None)
        self.build = get_object_or_404( Building,
            slug = self.kwargs['build_slug'] )
        if not self.build == plan.build:
            raise Http404(_("Plan does not belong to Building"))
        return plan

    def get_success_url(self):
        if 'add_another' in self.request.POST:
            return (reverse('bimblog:buildingplan_create',
                kwargs={'slug': self.build.slug}) +
                f'?plan_modified={self.object.title}')
        else:
            return (reverse('bimblog:building_detail',
                kwargs={'slug': self.build.slug}) +
                f'?plan_modified={self.object.title}')

class BuildingPlanDeleteView(PermissionRequiredMixin, FormView):
    model = BuildingPlan
    permission_required = 'bimblog.delete_buildingplan'
    form_class = BuildingPlanDeleteForm
    template_name = 'bimblog/buildingplan_form_delete.html'

    def setup(self, request, *args, **kwargs):
        super(BuildingPlanDeleteView, self).setup(request, *args, **kwargs)
        self.build = get_object_or_404( Building,
            slug = self.kwargs['build_slug'] )
        self.plan = get_object_or_404( BuildingPlan,
            slug = self.kwargs['plan_slug'] )
        if not self.build == self.plan.build:
            raise Http404(_("Plan does not belong to Building"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.plan.title
        return context

    def form_valid(self, form):
        self.plan.delete()
        return super(BuildingPlanDeleteView, self).form_valid(form)

    def get_success_url(self):
        return (reverse('bimblog:building_detail',
            kwargs={'slug': self.build.slug}) +
            f'?plan_deleted={self.plan.title}')

class PhotoStationCreateView( PermissionRequiredMixin, CreateView ):
    model = PhotoStation
    permission_required = 'bimblog.add_photostation'
    form_class = PhotoStationCreateForm

    def setup(self, request, *args, **kwargs):
        super(PhotoStationCreateView, self).setup(request, *args, **kwargs)
        #here we get the project by the slug
        self.build = get_object_or_404( Building, slug = self.kwargs['slug'] )

    def get_initial(self):
        initial = super( PhotoStationCreateView, self ).get_initial()
        initial['build'] = self.build.id
        initial['lat'] = self.build.lat
        initial['long'] = self.build.long
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #we add the following to feed the map
        context['build'] = self.build
        context['mapbox_token'] = settings.MAPBOX_TOKEN

        return context

    def get_success_url(self):
        if 'add_another' in self.request.POST:
            return reverse('portfolio:station_create' ,
                kwargs={'slug': self.build.slug})
        else:
            return reverse('portfolio:building_detail' ,
                kwargs={'slug': self.build.slug})
