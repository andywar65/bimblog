from django.db import models
from django.conf import settings

def building_default_intro():
    return _('Another Building by %(website)s!') % {'website': settings.WEBSITE_NAME}

def photo_station_default_intro():
    return (_('Another photo station by %(sitename)s!') %
        {'sitename': settings.WEBSITE_NAME})
