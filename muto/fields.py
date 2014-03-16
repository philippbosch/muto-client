from django.db import models
from django.utils.six import with_metaclass
from . import transformer


class MutoVersionsAccessor(object):
    def __init__(self, key):
        self.key = key

    def __getattr__(self, attr):
        return_url = False
        if attr[-4:] == '_url':
            attr = attr[:-4]
            return_url = True

        iv = transformer.get_image_version(self.key, attr)

        if return_url:
            return iv.get('url', '')
        return iv


class MutoImage(object):
    def __init__(self, key):
        self.key = key
        self.versions = MutoVersionsAccessor(self.key)

    def __str__(self):
        return self.key



class MutoField(with_metaclass(models.SubfieldBase, models.CharField)):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        super(MutoField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, MutoImage):
            return value

        return MutoImage(value)

    def get_prep_value(self, value):
        return str(value)
