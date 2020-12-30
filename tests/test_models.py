import os
from datetime import datetime

from django.conf import settings
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from bimblog.models import Building, BuildingPlan, PhotoStation, StationImage

@override_settings(USE_I18N=False)
class BuildingModelTest(TestCase):
    """Testing all methods that don't need SimpleUploadedFile"""
    @classmethod
    def setUpTestData(cls):
        build = Building.objects.create(title='Building', )
        Building.objects.create(date=datetime.strptime('2020-05-09', '%Y-%m-%d'))
        stat = PhotoStation.objects.create(build=build, title='Station')

    def test_building_str_method(self):
        build = Building.objects.get(slug='building')
        self.assertEquals(build.__str__(), 'Building')

    def test_building_intro(self):
        build = Building.objects.get(slug='building')
        self.assertEquals(build.intro,
            f'Another Building by {settings.WEBSITE_NAME}!')

    def test_building_maps(self):
        build = Building.objects.get(slug='building')
        self.assertEquals(build.lat, settings.CITY_LAT )
        self.assertEquals(build.long, settings.CITY_LONG )
        self.assertEquals(build.zoom, settings.CITY_ZOOM )

    def test_building_str_method_no_title(self):
        build = Building.objects.get(date='2020-05-09')
        self.assertEquals(build.__str__(), 'Building-09-05-20')

    def test_building_get_full_path(self):
        build = Building.objects.get(slug='building')
        self.assertEquals(build.get_full_path(), '/buildings/building/')

    def test_photostation_str_method(self):
        stat = PhotoStation.objects.get(slug='station')
        self.assertEquals(stat.__str__(), 'Station / Building')

    def test_photostation_intro(self):
        stat = PhotoStation.objects.get(slug='station')
        self.assertEquals(stat.intro,
            f'Another photo station by {settings.WEBSITE_NAME}!')

#@override_settings(MEDIA_ROOT=os.path.join(settings.MEDIA_ROOT, 'temp'))
#class StationImageTest(TestCase):
    #@classmethod
    #def setUpTestData(cls):
        #build = Building.objects.create(title='Building', intro = 'Foo',
            #body = 'Bar', site = 'Somewhere', category = 'ALT',
            #type = 'ALT', status = 'ALT', cost = 'ALT', )
        #stat = PhotoStation.objects.create(build=build, title='Station')
        #img_path = os.path.join(settings.STATIC_ROOT,
            #'portfolio/sample/image.jpg')
        #with open(img_path, 'rb') as f:
            #content = f.read()
        #statimg = StationImage.objects.create(stat_id=stat.id,
            #image=SimpleUploadedFile('image.jpg', content, 'image/jpg'))

    #def tearDown(self):
        #"""Checks existing files, then removes them"""
        #try:
            #list = os.listdir(os.path.join(settings.MEDIA_ROOT,
                #'uploads/images/galleries/'))
        #except:
            #return
        #for file in list:
            #os.remove(os.path.join(settings.MEDIA_ROOT,
                #f'uploads/images/galleries/{file}'))

    #def test_stationimage_fb_image(self):
        #image = StationImage.objects.get(image='uploads/images/galleries/image.jpg')
        #self.assertEquals(image.fb_image.path, 'uploads/images/galleries/image.jpg')
