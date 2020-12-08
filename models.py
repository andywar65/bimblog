import uuid
from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.urls import reverse
from django.core.validators import FileExtensionValidator

from filebrowser.fields import FileBrowseField
from filebrowser.base import FileObject

from project.utils import generate_unique_slug
from .map_utils import workflow
#from .choices import *
#from .map_utils import workflow

def building_default_intro():
    return _('Another Building by %(website)s!') % {'website': settings.WEBSITE_NAME}

class Building(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=100, editable=False, null=True)
    image = models.ImageField(_("Image"), max_length=200,
        null=True, upload_to='uploads/buildings/images/')
    fb_image = FileBrowseField(_("Image"), max_length=200,
        extensions=[".jpg", ".png", ".jpeg", ".gif", ".tif", ".tiff"],
        null=True, directory='buildings/images/')
    title = models.CharField(_('Title'),
        help_text=_("Building name"),
        max_length = 50, null=True, blank=True)
    intro = models.CharField(_('Introduction'),
        default = building_default_intro,
        help_text = _('Few words to describe this building'),
        max_length = 100)
    date = models.DateField(_('Date'), default = now, )
    last_updated = models.DateTimeField(editable=False, null=True)
    address = models.CharField(_('Address'), null=True, blank=True,
        help_text = _('Something like "Rome - Monteverde" is ok'),
        max_length = 100)
    lat = models.FloatField(_("Latitude"), default = 41.8988)
    long = models.FloatField(_("Longitude"), default = 12.5451,
        help_text=_("Coordinates from Google Maps or https://openstreetmap.org"))
    zoom = models.FloatField(_("Zoom factor"), default = 10,
        help_text=_("Maximum should be 21"))


    def __str__(self):
        return self.title

    def get_full_path(self):
        return reverse('bimblog:building_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = _('Building-%(date)s') % {'date': self.date.strftime("%d-%m-%y")}
        if not self.slug:
            self.slug = generate_unique_slug(Building, self.title)
        self.last_updated = now()
        super(Building, self).save(*args, **kwargs)
        if self.image and not self.fb_image:
            #save with filebrowser image, sloppy workaround to make working test
            Building.objects.filter(id=self.id).update(fb_image=FileObject(str(self.image)))

    class Meta:
        verbose_name = _('Building')
        verbose_name_plural = _('Buildings')
        ordering = ('-date', )

class BuildingPlan(models.Model):

    build = models.ForeignKey(Building, on_delete = models.CASCADE,
        related_name='building_plan', verbose_name = _('Building'))
    title = models.CharField(_('Name'),
        help_text=_("Name of the building plan"), max_length = 50, )
    slug = models.SlugField(max_length=100, editable=False, null=True)
    elev = models.FloatField(_("Elevation in meters"), default = 0)
    file = models.FileField(_("DXF file"), max_length=200,
        upload_to="uploads/buildings/plans/dxf/",
        validators=[FileExtensionValidator(allowed_extensions=['dxf', ])])
    geometry = models.JSONField( editable=False, null=True, blank=True )

    def __str__(self):
        return self.title + ' | ' + str(self.elev)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(BuildingPlan,
                self.title + ' ' + str(self.elev))
        #upload file
        super(BuildingPlan, self).save(*args, **kwargs)
        self.geometry = workflow(self.file, self.build.lat, self.build.long)
        #save geometry
        super(BuildingPlan, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Building plan')
        verbose_name_plural = _('Building plans')
        ordering = ('-elev', )
