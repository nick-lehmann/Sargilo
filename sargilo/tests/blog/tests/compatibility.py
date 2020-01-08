import django


DJANGO_VERSION = django.get_version()
DJANGO_VERSION_PARTS = list(map(int, DJANGO_VERSION.split('.')))
DJANGO_NOT_SUPPORTED = (
        DJANGO_VERSION_PARTS[0] > 1 or
        DJANGO_VERSION_PARTS[0] == 1 and DJANGO_VERSION_PARTS[1] > 7
)
DJANGO_ERROR = 'Django version {} is currently not supported'.format(DJANGO_VERSION)
