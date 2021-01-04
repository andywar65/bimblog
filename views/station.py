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
from bimblog.forms import ( PhotoStationCreateForm,
    PhotoStationDeleteForm, StationImageCreateForm, StationImageUpdateForm,
    StationImageDeleteForm )

class PhotoStationCreateView( PermissionRequiredMixin, CreateView ):
    model = PhotoStation
    permission_required = 'bimblog.add_photostation'
    form_class = PhotoStationCreateForm

    def setup(self, request, *args, **kwargs):
        super(PhotoStationCreateView, self).setup(request, *args, **kwargs)
        #here we get the building by the slug
        self.build = get_object_or_404( Building, slug = self.kwargs['slug'] )

    def get_initial(self):
        initial = super( PhotoStationCreateView, self ).get_initial()
        initial['build'] = self.build.id
        initial['lat'] = self.build.lat
        initial['long'] = self.build.long
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'stat_created' in self.request.GET:
            context['stat_created'] = self.request.GET['stat_created']
        elif 'stat_modified' in self.request.GET:
            context['stat_modified'] = self.request.GET['stat_modified']
        #we add the following to feed the map
        context['build'] = self.build
        context['plans'] = context['build'].building_plan.all()
        context['mapbox_token'] = settings.MAPBOX_TOKEN

        return context

    def get_success_url(self):
        if 'add_another' in self.request.POST:
            return (reverse('bimblog:station_create',
                kwargs={'slug': self.build.slug}) +
                f'?stat_created={self.object.title}')
        else:
            return (reverse('bimblog:building_detail',
                kwargs={'slug': self.build.slug}) +
                f'?stat_created={self.object.title}')

class PhotoStationDetailView( PermissionRequiredMixin, DetailView):
    model = PhotoStation
    permission_required = 'bimblog.view_photostation'
    context_object_name = 'stat'
    slug_field = 'slug'
    slug_url_kwarg = 'stat_slug'

    def get_object(self, queryset=None):
        obj = super(PhotoStationDetailView, self).get_object(queryset=None)
        build = get_object_or_404( Building, slug = self.kwargs['build_slug'] )
        if not build == obj.build:
            raise Http404(_("Station does not belong to Building"))
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'stat_created' in self.request.GET:
            context['stat_created'] = self.request.GET['stat_created']
        elif 'stat_modified' in self.request.GET:
            context['stat_modified'] = self.request.GET['stat_modified']
        elif 'img_created' in self.request.GET:
            context['img_created'] = self.request.GET['img_created']
        elif 'img_modified' in self.request.GET:
            context['img_modified'] = self.request.GET['img_modified']
        elif 'img_deleted' in self.request.GET:
            context['img_deleted'] = self.request.GET['img_deleted']
        #we add the following to feed the gallery
        context['main_gal_slug'] = get_random_string(7)
        #gallery images
        if 'reverse' in self.request.GET:
            context['reverse'] = self.request.GET['reverse']
            context['images'] = self.object.station_image.all().reverse()
        else:
            context['images'] = self.object.station_image.all()
        return context

class PhotoStationUpdateView( PermissionRequiredMixin, UpdateView ):
    model = PhotoStation
    permission_required = 'bimblog.change_photostation'
    form_class = PhotoStationCreateForm
    template_name = 'bimblog/photostation_form_update.html'
    #we have two slugs, so we need to override next attribute
    slug_url_kwarg = 'stat_slug'

    def get_object(self, queryset=None):
        #elsewhere we get the parent in setup, but here we also need object
        stat = super(PhotoStationUpdateView, self).get_object(queryset=None)
        self.build = get_object_or_404( Building,
            slug = self.kwargs['build_slug'] )
        if not self.build == stat.build:
            raise Http404(_("Station does not belong to Building"))
        return stat

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plans'] = self.build.building_plan.all()
        context['mapbox_token'] = settings.MAPBOX_TOKEN
        return context

    def get_success_url(self):
        if 'add_another' in self.request.POST:
            return (reverse('bimblog:station_create',
                kwargs={'slug': self.build.slug}) +
                f'?stat_modified={self.object.title}')
        else:
            return (reverse('bimblog:station_detail',
                kwargs={'build_slug': self.build.slug,
                'stat_slug': self.object.slug}) +
                f'?stat_modified={self.object.title}')

class PhotoStationDeleteView(PermissionRequiredMixin, FormView):
    #model = PhotoStation
    permission_required = 'bimblog.delete_photostation'
    form_class = PhotoStationDeleteForm
    template_name = 'bimblog/photostation_form_delete.html'

    def setup(self, request, *args, **kwargs):
        super(PhotoStationDeleteView, self).setup(request, *args, **kwargs)
        self.build = get_object_or_404( Building,
            slug = self.kwargs['build_slug'] )
        self.stat = get_object_or_404( PhotoStation,
            slug = self.kwargs['stat_slug'] )
        if not self.build == self.stat.build:
            raise Http404(_("Station does not belong to Building"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.stat.title
        return context

    def form_valid(self, form):
        self.stat.delete()
        return super(PhotoStationDeleteView, self).form_valid(form)

    def get_success_url(self):
        return (reverse('bimblog:building_detail',
            kwargs={'slug': self.build.slug}) +
            f'?stat_deleted={self.stat.title}')

class StationImageCreateView( PermissionRequiredMixin, CreateView ):
    model = StationImage
    permission_required = 'bimblog.add_stationimage'
    form_class = StationImageCreateForm

    def setup(self, request, *args, **kwargs):
        super(StationImageCreateView, self).setup(request, *args, **kwargs)
        #here we get the project by the slug
        self.build = get_object_or_404( Building, slug = self.kwargs['build_slug'] )
        self.stat = get_object_or_404( PhotoStation, slug = self.kwargs['stat_slug'] )
        if not self.stat.build == self.build:
            raise Http404(_("Station does not belong to Building"))

    def get_initial(self):
        initial = super( StationImageCreateView, self ).get_initial()
        initial['stat'] = self.stat.id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'img_created' in self.request.GET:
            context['img_created'] = self.request.GET['img_created']
        elif 'img_modified' in self.request.GET:
            context['img_modified'] = self.request.GET['img_modified']
        return context

    def get_success_url(self):
        if 'add_another' in self.request.POST:
            return (reverse('bimblog:image_add',
                kwargs={'build_slug': self.build.slug,
                'stat_slug': self.stat.slug}) +
                f'?img_created={self.object.id}')
        else:
            return (reverse('bimblog:station_detail',
                kwargs={'build_slug': self.build.slug,
                'stat_slug': self.stat.slug}) +
                f'?img_created={self.object.id}')

class StationImageUpdateView( PermissionRequiredMixin, UpdateView ):
    model = StationImage
    permission_required = 'bimblog.change_stationimage'
    form_class = StationImageUpdateForm
    template_name = 'bimblog/stationimage_form_update.html'

    def get_object(self, queryset=None):
        #elsewhere we get the parent in setup, but here we also need object
        img = super(StationImageUpdateView, self).get_object(queryset=None)
        self.build = get_object_or_404( Building, slug = self.kwargs['build_slug'] )
        self.stat = get_object_or_404( PhotoStation, slug = self.kwargs['stat_slug'] )
        if not self.stat.build == self.build:
            raise Http404(_("Station does not belong to Building"))
        if not self.stat == img.stat:
            raise Http404(_("Image does not belong to Photo Station"))
        return img

    def get_success_url(self):
        if 'add_another' in self.request.POST:
            return (reverse('bimblog:image_add',
                kwargs={'build_slug': self.build.slug,
                'stat_slug': self.stat.slug}) +
                f'?img_modified={self.object.id}')
        else:
            return (reverse('bimblog:station_detail',
                kwargs={'build_slug': self.build.slug,
                'stat_slug': self.stat.slug}) +
                f'?img_modified={self.object.id}')

class StationImageDeleteView(PermissionRequiredMixin, FormView):
    permission_required = 'bimblog.delete_stationimage'
    form_class = StationImageDeleteForm
    template_name = 'bimblog/stationimage_form_delete.html'

    def setup(self, request, *args, **kwargs):
        super(StationImageDeleteView, self).setup(request, *args, **kwargs)
        self.build = get_object_or_404( Building,
            slug = self.kwargs['build_slug'] )
        self.stat = get_object_or_404( PhotoStation,
            slug = self.kwargs['stat_slug'] )
        self.img = get_object_or_404( StationImage, id = self.kwargs['pk'])
        if not self.build == self.stat.build:
            raise Http404(_("Station does not belong to Building"))
        if not self.stat == self.img.stat:
            raise Http404(_("Image does not belong to Photo Station"))
        self.title = self.img.id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def form_valid(self, form):
        self.img.delete()
        return super(StationImageDeleteView, self).form_valid(form)

    def get_success_url(self):
        return (reverse('bimblog:station_detail',
            kwargs={'build_slug': self.build.slug, 'stat_slug': self.stat.slug}) +
            f'?img_deleted={self.title}')

class StationImageDayArchiveView( PermissionRequiredMixin, DayArchiveView ):
    model = StationImage
    permission_required = 'bimblog.view_stationimage'
    date_field = 'date'
    allow_future = True
    context_object_name = 'images'
    year_format = '%Y'
    month_format = '%m'
    day_format = '%d'
    allow_empty = True

    def setup(self, request, *args, **kwargs):
        super(StationImageDayArchiveView, self).setup(request, *args, **kwargs)
        #here we get the project by the slug
        self.build = get_object_or_404( Building, slug = self.kwargs['slug'] )

    def get_queryset(self):
        qs = super(StationImageDayArchiveView, self).get_queryset()
        #here we get the station ids by project related name
        stations = self.build.building_station.values_list('id', flat = True)
        return qs.filter( stat__in = stations )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #we add the following to feed the gallery
        context['main_gal_slug'] = get_random_string(7)
        context['build'] = self.build
        return context
