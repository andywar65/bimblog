from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext as _

from .models import Building

class BuildingCreateForm(ModelForm):
    image = forms.ImageField(label=_('Image'), required=True)

    class Meta:
        model = Building
        fields = ( 'image', 'title', 'intro', 'date', 'address', 'lat', 'long',
            'zoom')
