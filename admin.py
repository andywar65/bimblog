from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Building
#from pages.admin import GalleryImageInline

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', )
    #inlines = [ GalleryImageInline,  ]

    fieldsets = (
        (None, {
            'fields': ('title', 'date', 'intro', 'address'),
        }),
        (_('Map'), {
            'fields': ('lat', 'long', 'zoom', ),
        }),
        )
