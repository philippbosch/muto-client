# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from .models import ImageVersionDefinition


class ImageVersionDefinitionAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'description', 'user',)


admin.site.register(ImageVersionDefinition, ImageVersionDefinitionAdmin)


class MutoAdminThumbnailMixin(object):  # TODO
    def thumbnail(self, instance):
        size = 'small'
        if instance.pk is None:
            return ''
        version = instance.image_versions.get(size, None)
        if version is None:
            url = 'http://placehold.it/{0}x{1}/eee/ddd'.format(*settings.MUTO_SIZES[size])
        else:
            url = version.url
        return u'<div class="muto-thumb" style="width: {1}px; height: {2}px;"><img src="{0}"></div>'.format(url, *settings.MUTO_SIZES[size])

    thumbnail.allow_tags = True
    thumbnail.short_description = 'image'

    class Media:
        css = {
            'all': ['muto/admin-thumbnails.css']
        }
