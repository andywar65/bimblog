from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext as _

from .models import Building, BuildingPlan

class BuildingCreateForm(ModelForm):
    image = forms.ImageField(label=_('Image'), required=True)

    class Meta:
        model = Building
        fields = ( 'image', 'title', 'intro', 'date', 'address', 'lat', 'long',
            'zoom')

class BuildingUpdateForm(ModelForm):

    class Meta:
        model = Building
        fields = ( 'title', 'intro', 'date', 'address', 'lat', 'long',
            'zoom')

class BuildingDeleteForm(forms.Form):
    delete = forms.BooleanField( label=_("Delete the building"), required = True,
        help_text = _("""Caution, can't undo this."""))

class BuildingPlanCreateForm(ModelForm):
    build = forms.ModelChoiceField( label=_('Building'),
        queryset=Building.objects.all(), disabled = True )

    class Meta:
        model = BuildingPlan
        fields = '__all__'

class BuildingPlanDeleteForm(forms.Form):
    delete = forms.BooleanField( label=_("Delete the building plan"),
        required = True,
        help_text = _("""Caution, can't undo this."""))
