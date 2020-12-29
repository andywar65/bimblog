from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Building, BuildingPlan, PhotoStation, StationImage

class BuildingPlanInline(admin.TabularInline):
    model = BuildingPlan
    fields = ('title', 'elev', 'file', 'refresh', 'geometry', 'visible')
    extra = 0

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', )
    inlines = [ BuildingPlanInline,  ]

    fieldsets = (
        (_('Image'), {
            'fields': ('fb_image', ),
        }),
        (None, {
            'fields': ('title', 'date', 'intro', 'address'),
        }),
        (_('Map'), {
            'fields': ('lat', 'long', 'zoom', ),
        }),
        )

class StationImageInline(admin.TabularInline):
    model = StationImage
    fields = ('date', 'fb_image', 'caption', )
    extra = 0

@admin.register(PhotoStation)
class PhotoStationAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'intro', 'build', 'plan', 'lat', 'long')
    list_editable = ( 'lat', 'long')
    inlines = [ StationImageInline,  ]
