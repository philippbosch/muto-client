from collections import OrderedDict
import json

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField


class ImageVersionDefinition(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, related_name='image_version_definitions', help_text='If no user is selected, this image version will be availble to all users.')
    identifier = models.SlugField(max_length=64, db_index=True)
    description = models.CharField(max_length=64)
    options = JSONField(load_kwargs={'object_pairs_hook': OrderedDict}, default=json.dumps({'size': [320,240]}, indent=2))

    class Meta:
        unique_together = ('user', 'identifier',)
