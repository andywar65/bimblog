import json

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

from bimblog.models import Building, BuildingPlan, PhotoStation, StationImage
from bimblog.forms import ( BuildingCreateForm, BuildingUpdateForm,
    BuildingDeleteForm, BuildingPlanCreateForm, )

class BuildingListCreateView( PermissionRequiredMixin, CreateView ):
    model = Building
    permission_required = 'bimblog.view_building'
    form_class = BuildingCreateForm
    template_name = 'bimblog/building_list_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #list all buildings
        context['builds'] = Building.objects.all()
        #building alerts
        if 'created' in self.request.GET:
            context['created'] = self.request.GET['created']
        elif 'modified' in self.request.GET:
            context['modified'] = self.request.GET['modified']
        elif 'deleted' in self.request.GET:
            context['deleted'] = self.request.GET['deleted']
        #we add the following to feed the map
        #not using values() because we have to manipulate entries
        builds = []
        for build in context['builds']:
            build.fb_image.version_generate("medium")
            fb_path = (settings.MEDIA_URL +
                build.fb_image.version_path("medium"))
            builds.append({'title': build.title, 'intro': build.intro,
                'path': build.get_full_path(), 'lat': build.lat,
                'long': build.long, 'fb_path': fb_path})
        context['map_data'] = json.dumps({'builds': builds,
            'city_lat': settings.CITY_LAT,
            'city_long': settings.CITY_LONG,
            'city_zoom': settings.CITY_ZOOM,
            'mapbox_token': settings.MAPBOX_TOKEN})
        return context

    def form_valid(self, form):
        if not self.request.user.has_perm('bimblog.add_building'):
            raise Http404(_("User has no permission to add buildings"))
        return super(BuildingListCreateView, self).form_valid(form)

    def get_success_url(self):
        if 'add_another' in self.request.POST:
            return (reverse('bimblog:building_list') +
                f'?created={self.object.title}')
        else:
            return (reverse('bimblog:building_detail',
                kwargs={'slug': self.object.slug }) +
                f'?created={self.object.title}')

class BuildingDetailView(PermissionRequiredMixin, DetailView):
    model = Building
    permission_required = 'bimblog.view_building'
    context_object_name = 'build'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #add plans and stations
        context['plans'] = context['build'].building_plan.all()
        context['stations'] = context['build'].building_station.all()
        #add station lists
        context['stat_list'] = {}
        context['stat_list']['all'] = context['stations'].values_list('id')
        #add dates for images by date
        context['dates'] = StationImage.objects.filter(stat_id__in=context['stat_list']['all']).dates('date', 'day')
        #add alerts
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
        #elif 'stat_created' in self.request.GET:
            #context['stat_created'] = self.request.GET['stat_created']
        #elif 'stat_modified' in self.request.GET:
            #context['stat_modified'] = self.request.GET['stat_modified']
        elif 'stat_deleted' in self.request.GET:
            context['stat_deleted'] = self.request.GET['stat_deleted']
        #we add the following to feed the map
        #building data
        context['build'].fb_image.version_generate("medium")
        fb_path = (settings.MEDIA_URL +
            context['build'].fb_image.version_path("medium"))
        build = {'title': context['build'].title,
            'intro': context['build'].intro,
            'lat': context['build'].lat, 'long': context['build'].long,
            'zoom': context['build'].zoom,
            'fb_path': fb_path}
        #plan data
        plans = []
        for plan in context['plans']:
            plans.append({'id': plan.id, 'geometry': plan.geometry})
        #station data
        stations = []
        for stat in context['stations']:
            stat.station_image.first().fb_image.version_generate("medium")
            fb_path = (settings.MEDIA_URL +
                stat.station_image.first().fb_image.version_path("medium"))
            path = reverse('bimblog:station_detail',
                kwargs={'build_slug': context['build'].slug,
                'stat_slug': stat.slug})
            stations.append({'id': stat.id, 'title': stat.title, 'path': path,
                'fb_path': fb_path, 'lat': stat.lat, 'long': stat.long,
                'intro': stat.intro})
        #add stations that don't belong to plans
        no_plan = context['stations'].filter(plan_id=None)
        if no_plan:
            context['no_plan'] = no_plan
        context['map_data'] = json.dumps({
            'build': build,
            'plans': plans,
            'stations': stations,
            'no_plan_trans': _("No plan"),
            'mapbox_token': settings.MAPBOX_TOKEN})
        return context

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
            return (reverse('bimblog:building_list') +
                f'?modified={self.object.title}')
        else:
            return (reverse('bimblog:building_detail',
                kwargs={'slug': self.object.slug }) +
                f'?modified={self.object.title}')

class BuildingDeleteView(PermissionRequiredMixin, FormView):
    #model = Building
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
        if not 'cancel' in self.request.POST:
            self.build.delete()
        return super(BuildingDeleteView, self).form_valid(form)

    def get_success_url(self):
        if 'cancel' in self.request.POST:
            return reverse('bimblog:building_detail',
                kwargs={'slug': self.build.slug })
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
    #model = BuildingPlan
    permission_required = 'bimblog.delete_buildingplan'
    form_class = BuildingDeleteForm
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
        if not 'cancel' in self.request.POST:
            self.plan.delete()
        return super(BuildingPlanDeleteView, self).form_valid(form)

    def get_success_url(self):
        if 'cancel' in self.request.POST:
            return reverse('bimblog:building_detail',
                kwargs={'slug': self.build.slug})
        return (reverse('bimblog:building_detail',
            kwargs={'slug': self.build.slug}) +
            f'?plan_deleted={self.plan.title}')
