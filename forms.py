from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext as _

from .models import Building, BuildingPlan, PhotoStation, StationImage

class BuildingCreateForm(ModelForm):
    image = forms.ImageField(label=_('Image'), required=True)

    class Meta:
        model = Building
        fields = ( 'image', 'title', 'intro', 'date', 'address', 'lat', 'long',
            'zoom')

class BuildingUpdateForm(ModelForm):

    class Meta:
        model = Building
        fields = ( 'image', 'title', 'intro', 'date', 'address', 'lat', 'long',
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

class PhotoStationCreateForm(ModelForm):
    build = forms.ModelChoiceField( label=_('Building'),
        queryset=Building.objects.all(), disabled = True )

    class Meta:
        model = PhotoStation
        fields = '__all__'

    def __init__(self, **kwargs):
        super(PhotoStationCreateForm, self).__init__(**kwargs)
        #filter plan queryset
        self.fields['plan'].queryset = BuildingPlan.objects.filter(build_id=self.initial['build'])

class PhotoStationDeleteForm(forms.Form):
    delete = forms.BooleanField( label=_("Delete photo station"),
        required = True,
        help_text = _("""Caution, can't undo this."""))

class StationImageCreateForm(ModelForm):
    stat = forms.ModelChoiceField( label=_('Photo station'),
        queryset=PhotoStation.objects.all(), disabled = True )
    image = forms.ImageField(label=_('Image'), required=True)

    class Meta:
        model = StationImage
        fields = ( 'stat', 'date', 'image', 'caption')

class StationImageUpdateForm(ModelForm):
    stat = forms.ModelChoiceField( label=_('Photo station'),
        queryset=PhotoStation.objects.all(), disabled = True )

    class Meta:
        model = StationImage
        fields = ( 'image', 'stat', 'date', 'caption')
