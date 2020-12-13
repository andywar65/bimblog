from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Building, BuildingPlan, PhotoStation

class BuildingPlanInline(admin.TabularInline):
    model = BuildingPlan
    fields = ('title', 'elev', 'file')
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

@admin.register(PhotoStation)
class PhotoStationAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'intro', 'build', 'plan', 'lat', 'long')
    list_editable = ( 'lat', 'long')
