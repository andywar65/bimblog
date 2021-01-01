import os
from datetime import datetime

from django.conf import settings
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

from bimblog.models import Building, BuildingPlan, PhotoStation, StationImage
from users.models import User

@override_settings(USE_I18N=False)
@override_settings(MEDIA_ROOT=os.path.join(settings.MEDIA_ROOT, 'temp'))
class ProjectViewsTest(TestCase):
    """Testing all methods that don't need SimpleUploadedFile"""
    @classmethod
    def setUpTestData(cls):
        img_path = os.path.join(settings.STATIC_ROOT,
            'bimblog/images/image.jpg')
        with open(img_path, 'rb') as f:
            content = f.read()
        build = Building.objects.create(title='Building',
            image=SimpleUploadedFile('image.jpg', content, 'image/jpg'))
        Building.objects.create(date=datetime.strptime('2020-05-09', '%Y-%m-%d'),
            image=SimpleUploadedFile('image2.jpg', content, 'image/jpg'))
        dxf_path = os.path.join(settings.STATIC_ROOT,
            'bimblog/dxf/sample.dxf')
        with open(dxf_path, 'rb') as d:
            content_d = d.read()
        BuildingPlan.objects.create(build=build, title='Plan 1',
            file=SimpleUploadedFile('plan1.dxf', content_d, 'text/dxf'))
        stat = PhotoStation.objects.create(build=build, title='Station')
        PhotoStation.objects.create(build=build, title='Station 2')
        StationImage.objects.create(stat_id=stat.id,
            image=SimpleUploadedFile('image3.jpg', content, 'image/jpg'))
        noviewer = User.objects.create_user(username='noviewer',
            password='P4s5W0r6')
        viewer = User.objects.create_user(username='viewer',
            password='P4s5W0r6')
        adder = User.objects.create_user(username='adder',
            password='P4s5W0r6')
        permissions = Permission.objects.filter(
            codename__in=['view_building', 'view_buildingplan',
            'view_photostation', 'view_stationimage'])
        for p in permissions:
            viewer.user_permissions.add(p)
        group = Group.objects.get(name='Project Manager')
        adder.groups.add(group)

    def tearDown(self):
        """Checks existing files, then removes them"""
        try:
            list = os.listdir(os.path.join(settings.MEDIA_ROOT,
                'uploads/buildings/images/'))
        except:
            return
        for file in list:
            os.remove(os.path.join(settings.MEDIA_ROOT,
                f'uploads/buildings/images/{file}'))
        try:
            list = os.listdir(os.path.join(settings.MEDIA_ROOT,
                'uploads/buildings/plans/dxf/'))
        except:
            return
        for file in list:
            os.remove(os.path.join(settings.MEDIA_ROOT,
                f'uploads/buildings/plans/dxf/{file}'))

    def test_list_and_detail_status_code_forbidden(self):
        self.client.post(reverse('front_login'), {'username':'noviewer',
            'password':'P4s5W0r6'})
        build = Building.objects.get(slug='building')
        stat = PhotoStation.objects.get(slug='station')
        response = self.client.get(reverse('bimblog:building_list'))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('bimblog:building_detail',
            kwargs={'slug': 'building'}))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('bimblog:station_detail',
            kwargs={'build_slug': 'building', 'stat_slug': 'station'}))
        self.assertEqual(response.status_code, 403)

    def test_list_and_detail_status_code_ok(self):
        self.client.post(reverse('front_login'), {'username':'viewer',
            'password':'P4s5W0r6'})
        build = Building.objects.get(slug='building')
        stat = PhotoStation.objects.get(slug='station')
        response = self.client.get(reverse('bimblog:building_list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('bimblog:building_detail',
            kwargs={'slug': 'building'}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('bimblog:station_detail',
            kwargs={'build_slug': 'building', 'stat_slug': 'station'}))
        self.assertEqual(response.status_code, 200)
