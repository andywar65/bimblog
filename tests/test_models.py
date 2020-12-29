import os
from datetime import datetime

from django.conf import settings
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from portfolio.models import Project, ProjectStation, StationImage

@override_settings(USE_I18N=False)
class ProjectModelTest(TestCase):
    """Testing all methods that don't need SimpleUploadedFile"""
    @classmethod
    def setUpTestData(cls):
        prog = Project.objects.create(title='Project', intro = 'Foo',
            body = 'Bar', site = 'Somewhere', category = 'ALT',
            type = 'ALT', status = 'ALT', cost = 'ALT', )
        Project.objects.create(date=datetime.strptime('2020-05-09', '%Y-%m-%d'))
        stat = ProjectStation.objects.create(prog=prog, title='Station')
        #StationImage.objects.create(stat_id=stat.id,
            #image='uploads/images/galleries/image.jpg')

    def test_project_str_method(self):
        prog = Project.objects.get(slug='project')
        self.assertEquals(prog.__str__(), 'Project')

    def test_project_str_method_no_title(self):
        prog = Project.objects.get(date='2020-05-09')
        self.assertEquals(prog.__str__(), 'Project-09-05-20')

    def test_project_get_full_path(self):
        prog = Project.objects.get(slug='project')
        self.assertEquals(prog.get_full_path(), '/projects/project/')

    def test_projectstation_str_method(self):
        stat = ProjectStation.objects.get(slug='station')
        self.assertEquals(stat.__str__(), 'Station / Project')

    def test_projectstation_intro(self):
        stat = ProjectStation.objects.get(slug='station')
        self.assertEquals(stat.intro,
            f'Another photo station by {settings.WEBSITE_NAME}!')

@override_settings(MEDIA_ROOT=os.path.join(settings.MEDIA_ROOT, 'temp'))
class StationImageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        prog = Project.objects.create(title='Project', intro = 'Foo',
            body = 'Bar', site = 'Somewhere', category = 'ALT',
            type = 'ALT', status = 'ALT', cost = 'ALT', )
        stat = ProjectStation.objects.create(prog=prog, title='Station')
        img_path = os.path.join(settings.STATIC_ROOT,
            'portfolio/sample/image.jpg')
        with open(img_path, 'rb') as f:
            content = f.read()
        statimg = StationImage.objects.create(stat_id=stat.id,
            image=SimpleUploadedFile('image.jpg', content, 'image/jpg'))

    def tearDown(self):
        """Checks existing files, then removes them"""
        try:
            list = os.listdir(os.path.join(settings.MEDIA_ROOT,
                'uploads/images/galleries/'))
        except:
            return
        for file in list:
            os.remove(os.path.join(settings.MEDIA_ROOT,
                f'uploads/images/galleries/{file}'))

    def test_stationimage_fb_image(self):
        image = StationImage.objects.get(image='uploads/images/galleries/image.jpg')
        self.assertEquals(image.fb_image.path, 'uploads/images/galleries/image.jpg')
