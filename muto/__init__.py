import json
import redis
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import curry
from .models import ImageVersionDefinition


class Transformer(object):
    registry = []

    def __init__(self):
        self.redis = redis.StrictRedis.from_url(getattr(settings, 'MUTO_REDIS_URL', 'redis://:6379'))

    def register(self, model, field, build_filter=None):
        def add_to_queue(sender, instance, field, **kwargs):
            payload = dict(
                model=str(model._meta),
                pk=instance.pk,
                field=field,
                bucket=getattr(settings, 'MUTO_AWS_STORAGE_BUCKET_NAME', getattr(settings, 'AWS_STORAGE_BUCKET_NAME')),
                key=str(getattr(instance, field)),
                versions=[],
                callback_url=getattr(settings, 'MUTO_CALLBACK_URL', None),
            )

            if callable(build_filter):
                filter = build_filter(instance)
                image_version_definitions = ImageVersionDefinition.objects.filter(filter)
            else:
                image_version_definitions = ImageVersionDefinition.objects.all()

            for ivd in image_version_definitions:
                payload['versions'].append(dict(
                    identifier=ivd.identifier,
                    options=ivd.options,
                ))

            self.redis.lpush('muto:queue', json.dumps(payload))
            self.redis.publish('muto:queue', 'PUSH')

        func = curry(add_to_queue, field=field)
        rcvr = receiver(post_save, sender=model)(func)
        self.registry.append(dict(
            receiver=rcvr,
            model=model,
            field=field,
        ))

    def get_image_version(self, key, identifier):
        version = self.redis.hgetall('muto:{bucket}:{key}:{version}'.format(**dict(
            bucket=settings.AWS_STORAGE_BUCKET_NAME,
            key=key,
            version=identifier,
        )))
        version['url'] = self.build_url(key, identifier)
        return version

    def build_url(self, key, identifier):
        key_base, key_ext = key.rsplit('.')
        version_key = u'{0}.{1}.{2}'.format(key_base, identifier, key_ext)

        return "http://{bucket}.s3.amazonaws.com/{key}".format(**dict(
            bucket=settings.AWS_STORAGE_BUCKET_NAME,
            key=version_key,
        ))


transformer = Transformer()
