from django.core.management.base import BaseCommand, CommandError
from apiserver.api import models, utils

import time

class Command(BaseCommand):
    help = 'Tasks to run on the portal daily. 7am UTC = 12am or 1am Calgary'

    def tally_active_members(self):
        all_members = models.Member.objects
        active_members = all_members.filter(paused_date__isnull=True)

        for member in active_members:
            utils.tally_membership_months(member)

        return active_members.count()


    def handle(self, *args, **options):
        start = time.time()
        count = self.tally_active_members()
        self.stdout.write('Tallied {} active members in {} s'.format(
            count, str(time.time() - start)
        ))
