from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext as _

from .models import (Building, BuildingPlan, PhotoStation, StationImage,
    Discipline, DisciplineNode)

class BuildingCreateForm(ModelForm):
    image = forms.ImageField(label=_('Image'), required=True)

    class Meta:
        model = Building
        fields = ( 'image', 'title', 'intro', 'date', 'address', 'lat', 'long',
            'zoom', 'disciplinesn')

class BuildingUpdateForm(ModelForm):

    class Meta:
        model = Building
        fields = ( 'image', 'title', 'intro', 'date', 'address', 'lat', 'long',
            'zoom', 'disciplinesn')

class BuildingDeleteForm(forms.Form):
    delete = forms.BooleanField( label=_("Delete the building"),
        required = False,
        help_text = _("""Caution, can't undo this."""))

class BuildingPlanCreateForm(ModelForm):
    build = forms.ModelChoiceField( label=_('Building'),
        queryset=Building.objects.all(), disabled = True )

    class Meta:
        model = BuildingPlan
        fields = '__all__'

class PhotoStationCreateForm(ModelForm):
    build = forms.ModelChoiceField( label=_('Building'),
        queryset=Building.objects.all(), disabled = True )

    def __init__(self, **kwargs):
        super(PhotoStationCreateForm, self).__init__(**kwargs)
        #filter plan queryset
        self.fields['plan'].queryset = BuildingPlan.objects.filter(build_id=self.initial['build'])

    class Meta:
        model = PhotoStation
        fields = '__all__'

class StationImageCreateForm(ModelForm):
    stat = forms.ModelChoiceField( label=_('Photo station'),
        queryset=PhotoStation.objects.all(), disabled = True )
    image = forms.ImageField(label=_('Image'), required=True)

    class Meta:
        model = StationImage
        fields = ( 'image', 'stat', 'date', 'caption')

class StationImageUpdateForm(ModelForm):
    stat = forms.ModelChoiceField( label=_('Photo station'),
        queryset=PhotoStation.objects.all(), disabled = True )

    class Meta:
        model = StationImage
        fields = ( 'image', 'stat', 'date', 'caption')

class DisciplineCreateForm(ModelForm):

    class Meta:
        model = Discipline
        fields = '__all__'

class DisciplineNodeCreateForm(forms.Form):
    parent = forms.ModelChoiceField( label=_('Parent discipline'),
        queryset=DisciplineNode.objects.all(), required=False )
    title = forms.CharField( label=_('Title'),
        help_text=_("Discipline name"),
        max_length = 50, required=True)
    intro = forms.CharField( label=_('Description'),
        required=False, empty_value=None,
        help_text = _('Few words to describe the discipline'),
        max_length = 100)

class DisciplineNodeUpdateForm(ModelForm):

    class Meta:
        model = DisciplineNode
        fields = ('title', 'intro')
