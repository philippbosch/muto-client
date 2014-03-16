from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError
from muto import transformer


class Command(NoArgsCommand):
    help = 'Re-generate image versions'

    def handle_noargs(self, **options):
        self.stdout.write('Generating image versions')
        for registrant in transformer.registry:
            self.stdout.write('-----> {0} '.format(str(registrant['model']._meta)), ending='')
            for instance in registrant['model'].objects.all():
                self.stdout.write('.', ending='')
                registrant['receiver'](sender=registrant['model'], instance=instance, field=registrant['field'])
            self.stdout.write('\n')
        self.stdout.write('Done.')
