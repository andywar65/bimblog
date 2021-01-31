from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext as _

def create_bimblog_group(sender, **kwargs):
    from django.contrib.auth.models import Permission, Group
    grp, created = Group.objects.get_or_create(name=_('Building Manager'))
    if created:
        permissions = Permission.objects.filter(codename__in=('view_building',
            'add_building', 'change_building', 'delete_building',
            'view_buildingplan', 'add_buildingplan', 'change_buildingplan',
            'delete_buildingplan',
            'view_photostation', 'add_photostation', 'change_photostation',
            'delete_photostation',
            'view_stationimage', 'add_stationimage', 'change_stationimage',
            'delete_stationimage', 'view_discipline', 'add_discipline',
            'change_discipline', 'delete_discipline', 'view_disciplinenode',
            'add_disciplinenode', 'change_disciplinenode',
            'delete_disciplinenode',))
        grp.permissions.set(permissions)

def create_disciplines(sender, **kwargs):
    from bimblog.models import DisciplineNode
    DisciplineNode.objects.get_or_create(title=_('Architecture'), depth=1, path='0001')
    DisciplineNode.objects.get_or_create(title=_('MEP'), depth=1, path='0002')
    DisciplineNode.objects.get_or_create(title=_('Structure'), depth=1, path='0003')

class BimblogConfig(AppConfig):
    name = 'bimblog'

    def ready(self):
        post_migrate.connect(create_bimblog_group, sender=self)
        post_migrate.connect(create_disciplines, sender=self)
